# ----- System imports
import pprint

# ----- Local imports
import time

from src.const.constants import *
from src.model.composing.dfs import DFSComposer
from src.util.browser import BrowserUtil
from src.util.gmail_api import GmailAPIUtil
from src.util.log import Logger
from src.util.orderedset import OrderedSet

body_route = '''Hello, dear

I found an {cool_status} route - it comes over {count_countries} countries for {price} rub, so the "cost/count" value is {cc} rub!

The route starts in the {start_point} and finishes in the {finish_point}.

It comes over next countries: {countries_visited}

The dump of the route:

{dump}

Search links:

{links}

TripMaker bot
'''


MAX_SEARCH_TIME_PER_PERIOD = 240

CHECK_ONLY_BIGGEST = True

pretty_printer = pprint.PrettyPrinter()

eu_airports_list = open(PATH_DATA_EU_AIRPORTS, 'r').read().splitlines()
eu_airports = [x.split("\t") for x in eu_airports_list]

# actual for 2017-02-16 23:16
# the first 6-th are the biggest
biggest_eu_airports_list = ['BRU', 'SOF', 'BLL', 'CPH', 'CGN', 'GDN', 'VIE', 'PFO', 'OSR', 'TLS', 'FRA', 'FMM', 'ATH',
                            'SKG', 'BUD', 'DUB', 'SNN', 'BLQ', 'PSA', 'VNO', 'TGD', 'EIN', 'OSL', 'KTW', 'KRK', 'WAW',
                            'WRO', 'FAO', 'OPO', 'TSR', 'BTS', 'ALC', 'BCN', 'MAD', 'MAN']

date_period_list = ["2017-02-01:month", "2017-03-01:month", "2017-04-01:month"]
list_big_airports = OrderedSet()

best_count_result = 0
best_cost_result = 0

counter = 0
for airport in eu_airports:
    counter += 1
    orig_iata = airport[0]
    if CHECK_ONLY_BIGGEST:
        if orig_iata not in biggest_eu_airports_list:
            continue

    Logger.error("#{}) Selected airport: {} ({}, {})    ".format(counter, *airport))

    period_count_result, period_cost_result, period_countries_result, period_route_result = 0, 0, {}, []
    for date_period in date_period_list:
        time_start_period = time.time()

        Logger.info("For airport {} selected period: {}".format(orig_iata, date_period))
        try:
            count_result, cost_result, countries_result, route_result = \
                DFSComposer().start(orig_iata, date_period, True, MAX_SEARCH_TIME_PER_PERIOD)
        except Exception as e:
            Logger.error("Caught very broad exception while processing {} for period {}. "
                         "Exception: {}".format(orig_iata, date_period, str(e)))
            continue

        if (len(countries_result) > period_count_result) \
                | ((len(countries_result) == period_count_result) & (cost_result < period_cost_result)):
            period_count_result = len(countries_result)
            period_cost_result = cost_result
            period_countries_result = countries_result
            period_route_result = route_result
        if time.time() - time_start_period > MAX_SEARCH_TIME_PER_PERIOD:
            Logger.info("Airport {} is soo big!".format(orig_iata))
            list_big_airports.add(orig_iata)

    if period_cost_result > 0:
        Logger.error("Best period result for {}: c/c={}, "
                     "visited {} countries for {} rub: {}".format(orig_iata,
                                                                  round(period_cost_result / period_count_result),
                                                                  period_count_result, period_cost_result,
                                                                  period_countries_result))
        Logger.info("The route:")
        Logger.info(period_route_result.to_json())

        cool_condition_1 = ((period_count_result >= 15) & (round(period_cost_result / period_count_result) <= 1000))
        cool_condition_2 = ((period_count_result > 10) & (round(period_cost_result / period_count_result) <= 500))
        if cool_condition_1 | cool_condition_2:
            cool_status = "AMAZINGLY COOL" if cool_condition_1 else "pretty cool"

            links_list = []
            for flight in period_route_result:
                links_list.append(BrowserUtil.create_link(flight))
            links_message = "\n".join(links_list)

            subject = "[TripMaker] {} route: {} countries, " \
                      "{} rub ({} r/c)".format(cool_status, period_count_result, period_cost_result,
                                               round(period_cost_result / period_count_result))

            start_point = "{} ({}, {})".format(*airport)
            finish_point = period_route_result[-1].dest_city

            body = body_route.format(count_countries=period_count_result, price=period_cost_result,
                                     cc=round(period_cost_result / period_count_result),
                                     start_point=start_point, finish_point=finish_point,
                                     countries_visited=period_countries_result, cool_status=cool_status,
                                     dump=period_route_result.to_json(), links=links_message)
            message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)

            GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
            Logger.error("Sending: {}".format(subject))
    else:
        Logger.info("Nothing found for {} ({}, {})".format(*airport))

    Logger.info("")

    if (len(countries_result) > best_count_result) \
            | ((len(countries_result) == best_count_result) & (cost_result < best_cost_result)):
        best_count_result = len(countries_result)
        best_cost_result = cost_result
        best_countries_result = countries_result
        best_route_result = route_result

message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com",
                                      "[TripMaker] Computations completed", "I finished. Restart me!")
GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)

Logger.info("List of big airports ({}): {}".format(len(list_big_airports), list_big_airports))

Logger.info("Best total result: visited {} countries for {} rub: {}".format(best_count_result,
                                                                            best_cost_result, best_countries_result))
Logger.info("The route:")
Logger.info(route_result.to_json())
