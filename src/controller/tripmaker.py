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

# RegEx:

# datetime\.datetime\(([0-9]+), ([0-9]+), ([0-9]+), [0-9]+, [0-9]+\)
# \1-\2-\3

# Dates with one-digit month
# ([0-9]{4}-)([0-9]{1})(-[0-9]{2})
# \1(0)\2\3

# Dates with one-digit day
# ([0-9]{4}-[0-9]{2}-)([0-9]{1})[^0-9]
# \1(0)\2

# Dates with both one-digit month and day
# ([0-9]{4}-)([0-9]{1}-)([0-9]{1})[^0-9]
# \1(0)\2(0)\3

# ,\r\n\s*?'trip_class': <SeatClass\.economic: 'economic'>
# <empty>
