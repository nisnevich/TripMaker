from datetime import datetime

from src.const.constants import DATE_FORMAT
from src.util.log import Logger
from src.util.log_analyser import LogAnalyseUtil
from src.util.progressbar import print_progress_bar

cheap_tip = ["BTS", "MUC", "MIL", "SKG", "NTE", "TLS", "MSQ", "CGN", "BER"]
# cheap_tip = ["BTS", "MUC", "MIL", "SKG", "NTE", "TLS", "MSQ", "CGN"]

# list_cities_origin = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ"]
list_cities_origin = ["MOW"]
logfile_names_list = ["main_test5_full.log", "main_test6_full (dfs only).log"]

routes = LogAnalyseUtil.get_routes(*logfile_names_list, min_countries_count=15,
                                   max_cc=1000)
# DTM
results = []
Logger.info("Mapping:")
counter = 0
for route in routes:
    counter += 1
    print_progress_bar(counter, len(routes),
                       prefix='Scanning routes', suffix='Completed',
                       length=50)
    # if route[0].orig_country == "DE":
    # if route[0].orig_city in cheap_tip:
    #     print("Found route from cheap tips - starts in {}!".format(route[0].orig_city))
    results.append(route)

if len(results) == 0:
    Logger.info("Sorry, found nothing")
for route in results:
    price = route.get_price_total()
    count = len(route.get_countries_visited())
    Logger.info("Mapping route: ({}-{} at {}-{}), {} countries, {} rub, c/c={} rub"
                "".format(route[0].orig_city, route[-1].dest_city,
                          datetime.strftime(route[0].depart_date, DATE_FORMAT),
                          datetime.strftime(route[-1].depart_date, DATE_FORMAT),
                          count, price, round(price / count)))
    Logger.debug(route.to_json())
