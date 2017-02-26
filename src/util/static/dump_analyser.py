import json
import webbrowser
from datetime import datetime

from src.const.constants import PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flightroute import FlightsRoute

# ------ Constants
from src.util.browser import BrowserUtil

RANGE_VALUE = 0

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

print("Count of flights: {}".format(len(route_flights)))
print("Count of visited countries: {}".format(len(route_flights.get_countries_visited())))
print("Total price: {}".format(route_flights.get_price_total()))
