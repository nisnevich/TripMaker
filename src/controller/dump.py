# ----- System imports
import json
import pprint
import time

# ----- Local imports
from collections import namedtuple

from src.const.constants import *
from src.entity.flightroute import FlightsRoute
from src.model.composing.dfs import DFSComposer
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.logging import Logger

pretty_printer = pprint.PrettyPrinter()
dfs_composer = DFSComposer()

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute(json.loads(dump))

visited_countries = {(f.orig_country, f.dest_country) for f in route_flights}
total_cost = sum([f.price for f in route_flights])

orig_iata = route_flights[-1].orig_city
start_time = time.time()
list_flights = get_lowest_prices_flights_list(orig_iata)
Logger.info(("Flights searching from {} for a '{}' period "
             "took {} seconds").format(orig_iata, ORIGIN_DATE_PERIOD, round(time.time() - start_time, 1)))

count_result, cost_result, countries_result, route_result = \
    dfs_composer.filter_flights(list_flights, visited_countries, route_flights, total_cost)

Logger.info("Best result: visited {} countries for {} rub: {}".format(count_result,
                                                                      cost_result, countries_result))
Logger.info("The route:")
Logger.info(pretty_printer.pformat([vars(obj) for obj in route_result]))
