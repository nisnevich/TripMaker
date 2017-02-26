from datetime import datetime

from jsonpickle import json

from src.const.constants import PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flightroute import FlightsRoute
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



# def send_email(route_total, default_mapping):
#     links_list = []
#     for flight in route_total:
#         links_list.append(BrowserUtil.create_link(flight))
#     links_message = "\n".join(links_list)
#
#     countries = route_total.get_countries_visited()
#     cost = route_total.get_price_total()
#     subject = "[TripMaker] Finish: {} countries, " \
#               "{} rub ({} r/c) ({})".format(len(countries), cost, round(cost / len(countries)), default_mapping)
#
#     orig_city = CountryUtil.get_info(route_total[0].orig_city)
#     dest_city = CountryUtil.get_info(route_total[-1].dest_city)
#     orig_city = "unknown city" if orig_city is None else orig_city["name"]
#     dest_city = "unknown city" if dest_city is None else dest_city["name"]
#
#     start_point = "{} ({}, {})".format(route_total[0].orig_city, orig_city, route_total[0].orig_country)
#     finish_point = "{} ({}, {})".format(route_total[-1].dest_city, dest_city, route_total[-1].dest_country)
#
#     body = body_route.format(count_countries=len(countries), price=cost,
#                              cc=round(cost / len(countries)),
#                              start_point=start_point, finish_point=finish_point,
#                              start_date=route_total[0].depart_date, finish_date=route_total[-1].depart_date,
#                              countries_visited=countries, dump=route_total.to_json(),
#                              links=links_message, default_mapping=default_mapping)
#     message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)
#
#     GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
#     Logger.error("Sending: {}".format(subject))
#
# dump = open(PATH_ROUTE_DUMP, 'r').read()
# route = FlightsRoute.from_json(json.loads(dump))
#
# mapping = "({}-{} at {}-{})".format(route[0].orig_city, route[-1].dest_city,
#                       datetime.strftime(route[0].depart_date, DATE_FORMAT),
#                       datetime.strftime(route[-1].depart_date, DATE_FORMAT))
#
# send_email(route, mapping)
