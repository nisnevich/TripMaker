# ----- System imports
import pprint

# ----- Local imports
from src.const.constants import *
from src.model.composing.dfs import DFSComposer
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.country import CountryUtil
from src.util.log import Logger

pretty_printer = pprint.PrettyPrinter()
dfs_composer = DFSComposer()

for orig_iata in DEFAULT_ORIGIN_IATA:
     count_result, cost_result, countries_result, route_result = \
        dfs_composer.start(DEFAULT_ORIGIN_IATA)

Logger.info("Best result: visited {} countries for {} rub: {}".format(count_result,
                                                                      cost_result, countries_result))
Logger.info("The route:")
Logger.info(route_result.to_json())
