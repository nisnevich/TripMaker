from datetime import timedelta, datetime

from src.const.constants import DATE_FORMAT
from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.browser import BrowserUtil
from src.util.country import CountryUtil
from src.util.gmail_api import GmailAPIUtil
from src.util.log import Logger

body_route = '''Hello, dear

I found a cool finish for your route - it comes over {count_countries} countries for {price} rub, so the "cost/count" value is {cc} rub!

The route starts in the {start_point} at {start_date} and finishes in the {finish_point} at {finish_date}.

It comes over next countries: {countries_visited}

Mapping: {default_mapping}

The dump of the route:

{dump}

Search links:

{links}

TripMaker bot
'''


class TargetCountryFlightFilter(FlightFilter):
    target_country = None
    min_delta_days_depart = 7
    max_delta_days_depart = 7

    max_price_total = 20000
    allowable_price_error = 0

    def __init__(self, target_country, allowable_error=0):
        super().__init__()
        self.target_country = target_country
        self.allowable_price_error = allowable_error

    def filter_continue(self, flight, list_flights, graph):
        date_min = flight.depart_date - timedelta(days=self.min_delta_days_depart)
        date_max = flight.depart_date + timedelta(days=self.max_delta_days_depart)

        if flight.dest_country == self.target_country and date_min < list_flights[-1].depart_date < date_max:
            Logger.info("[ATTENTION:TARGET_COUNTRY:MATCH_DATE] Make an attention to flight {} ({}) to {} "
                        "({}) (for {} rub) - date matched: {} <= {} <= {}!"
                        "".format(flight.orig_city, flight.orig_country, flight.dest_city, flight.dest_country,
                                  flight.price, datetime.strftime(date_min, DATE_FORMAT),
                                  datetime.strftime(flight.depart_date, DATE_FORMAT),
                                  datetime.strftime(date_max, DATE_FORMAT)))
            route_total = FlightsRoute(*list_flights, flight)
            Logger.info("Count of flights: {}".format(len(route_total)))
            Logger.info("Count of visited countries: {}".format(len(route_total.get_countries_visited())))
            Logger.info("Total price: {}".format(route_total.get_price_total()))
            mapping = "({}-{} at {}-{})".format(list_flights[0].orig_city, list_flights[-1].dest_city,
                      datetime.strftime(list_flights[0].depart_date, DATE_FORMAT),
                      datetime.strftime(list_flights[-1].depart_date, DATE_FORMAT))
            Logger.info("The docking route: {}".format(mapping), is_separate=True)
            price_total = list_flights.get_price_total() + flight.price
            if price_total <= self.max_price_total + self.allowable_price_error:
                Logger.info(("[ATTENTION:TARGET_COUNTRY] Flight from {} to {} (for {} rub) at {} is the flight to"
                             " {}, the target country!").format(flight.orig_city, flight.dest_city,
                                                                flight.price, flight.depart_date, flight.dest_country))
                Logger.info("Total route: ")
                Logger.info(route_total.to_json(), is_route=True)
                self.send_email(route_total, mapping)
            else:
                Logger.info(("[IGNORE:TARGET_COUNTRY:FAIL_PRICE] Unfortunately, the flight {} ({}) to {} ({}) "
                             "(for {} rub) is not for us: total price is {} rub, its too big!"
                             "").format(flight.orig_city, flight.orig_country, flight.dest_city,
                                        flight.dest_country,
                                        flight.price, flight.dest_city, price_total))
                return False

    def send_email(self, route_total, default_mapping):
        links_list = []
        for flight in route_total:
            links_list.append(BrowserUtil.create_link(flight))
        links_message = "\n".join(links_list)

        countries = route_total.get_countries_visited()
        cost = route_total.get_price_total()
        subject = "[TripMaker] Finish: {} countries, " \
                  "{} rub ({} r/c) ({})".format(len(countries), cost, round(cost / len(countries)), default_mapping)

        orig_city = CountryUtil.get_info(route_total[0].orig_city)
        dest_city = CountryUtil.get_info(route_total[-1].dest_city)
        orig_city = "unknown city" if orig_city is None else orig_city["name"]
        dest_city = "unknown city" if dest_city is None else dest_city["name"]

        start_point = "{} ({}, {})".format(route_total[0].orig_city, orig_city, route_total[0].orig_country)
        finish_point = "{} ({}, {})".format(route_total[-1].dest_city, dest_city, route_total[-1].dest_country)

        body = body_route.format(count_countries=len(countries), price=cost,
                                 cc=round(cost / len(countries)),
                                 start_point=start_point, finish_point=finish_point,
                                 start_date=route_total[0].depart_date, finish_date=route_total[-1].depart_date,
                                 countries_visited=countries, dump=route_total.to_json(),
                                 links=links_message, default_mapping=default_mapping)
        message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)

        GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
        Logger.error("Sending: {}".format(subject))