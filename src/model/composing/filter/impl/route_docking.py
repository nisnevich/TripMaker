from datetime import timedelta, datetime

from jsonpickle import json

from src.const.constants import DATE_FORMAT, PATH_ROUTE_DUMP
from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.browser import BrowserUtil
from src.util.country import CountryUtil
from src.util.gmail_api import GmailAPIUtil
from src.util.log import Logger

body_route = '''Hello, dear

I found a cool start for your route - it comes over {count_countries} countries for {price} rub, so the "cost/count" value is {cc} rub!

The route starts in the {start_point} at {start_date} and finishes in the {finish_point} at {finish_date}.

It comes over next countries: {countries_visited}

Mapping: {default_mapping}

The dump of the route:

{dump}

Search links:

{links}

TripMaker bot
'''


class DockingRouteFlightFilter(FlightFilter):

    def __init__(self, list_routes_docking, allowable_error=0):
        super().__init__()
        self.min_delta_days_depart = 7
        self.max_delta_days_depart = 7
        self.max_price_total = 20000
        self.list_routes_docking = list_routes_docking
        self.allowable_price_error = allowable_error
        Logger.info("Formed cities target list. Will ignore all other cities.")

    def filter_continue(self, flight, list_flights, graph):
        for route in self.list_routes_docking:
            flight_from = route[0]
            flight_to = route[-1]
            f1 = self.do_filter(flight_from.orig_city, flight_from.depart_date, route, flight, list_flights)
            # f2 = self.do_filter(flight_to.dest_city, flight_to.depart_date, route, flight, list_flights)
            if not f1:
                return False
        return True

    def do_filter(self, city, date, route, flight, list_flights):
        if flight.dest_city == city:
            date_min = date - timedelta(days=self.min_delta_days_depart)
            date_max = date + timedelta(days=self.max_delta_days_depart)
            if date_min <= flight.depart_date <= date_max:
                Logger.info("[ATTENTION:ROUTE_DOCKING:MATCH_DATE] Make an attention to flight {} ({}) to {} "
                            "({}) (for {} rub) - date matched: {} <= {} <= {}!"
                            "".format(flight.orig_city, flight.orig_country, flight.dest_city, flight.dest_country,
                                      flight.price, datetime.strftime(date_min, DATE_FORMAT),
                                      datetime.strftime(flight.depart_date, DATE_FORMAT),
                                      datetime.strftime(date_max, DATE_FORMAT)))
                route_total = FlightsRoute(*list_flights, flight, *route)
                Logger.info("Count of flights: {}".format(len(route_total)))
                Logger.info("Count of visited countries: {}".format(len(route_total.get_countries_visited())))
                Logger.info("Total price: {}".format(route_total.get_price_total()))
                mapping = "({}-{} at {}-{}) by city {}".format(route[0].orig_city, route[-1].dest_city,
                                      datetime.strftime(route[0].depart_date, DATE_FORMAT),
                                      datetime.strftime(route[-1].depart_date, DATE_FORMAT), city)
                Logger.info("The docking route: {}".format(mapping))
                price_total = route.get_price_total() + list_flights.get_price_total() + flight.price
                if price_total <= self.max_price_total + self.allowable_price_error:
                    Logger.info(("[ATTENTION:ROUTE_DOCKING:CITY_TARGET] The flight {} ({}) to {} ({}) "
                                 "(for {} rub): city {} is ok, total route cost - {} rub!"
                                 "").format(flight.orig_city, flight.orig_country, flight.dest_city,
                                            flight.dest_country,
                                            flight.price, flight.dest_city, price_total))
                    Logger.info("Total route: ")
                    Logger.info(route_total.to_json())
                    self.send_email(route_total, mapping)
                else:
                    Logger.info(("[IGNORE:ROUTE_DOCKING:FAIL_PRICE] Unfortunately, flight {} ({}) to {} ({}) "
                                 "(for {} rub) cannot be docked with the route - {} rub!"
                                 "").format(flight.orig_city, flight.orig_country, flight.dest_city,
                                            flight.dest_country,
                                            flight.price, price_total))
                    return False
        return True

    def send_email(self, route_total, default_mapping):
        links_list = []
        for flight in route_total:
            links_list.append(BrowserUtil.create_link(flight))
        links_message = "\n".join(links_list)

        countries = route_total.get_countries_visited()
        cost = route_total.get_price_total()
        subject = "[TripMaker] Start: {} countries, " \
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
