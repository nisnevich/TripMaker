# ----- System imports
import pprint
import time

# ----- Local imports
from src.const.constants import *
from src.model.composing.dfs import DFSComposer
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.country import CountryUtil
from src.util.logging import Logger

pretty_printer = pprint.PrettyPrinter()
dfs_composer = DFSComposer()

for orig_iata in DEFAULT_ORIGIN_IATA:
    start_time = time.time()
    list_flights = get_lowest_prices_flights_list(orig_iata)
    Logger.info(("Flights searching from {} for a '{}' period "
                 "took {} seconds").format(orig_iata, ORIGIN_DATE_PERIOD, round(time.time() - start_time, 1)))
    count_result, cost_result, countries_result, route_result = \
        dfs_composer.filter_flights(list_flights, {CountryUtil.get_country(orig_iata)})

Logger.info("Best result: visited {} countries for {} rub: {}".format(count_result,
                                                                      cost_result, countries_result))
Logger.info("The route:")
Logger.info(route_result.to_json())
