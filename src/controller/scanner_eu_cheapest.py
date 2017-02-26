# ----- System imports
import pprint

# ----- Local imports
import random
import time
from datetime import datetime
from threading import Thread

import matplotlib.pyplot as plt

import networkx as nx
from multiprocessing import Process

from src.const.constants import *
from src.controller.callable.docking_from_ru import StartDockingCallableController
from src.controller.callable.docking_to_ru import FinishDockingCallableController
from src.model.composing.dfs import DFSComposer
from src.model.composing.filter.impl.country_visited_exclude_cheap import VisitedCountryExcludeCheapFlightFilter
from src.model.composing.filter.impl.edge_visited import VisitedEdgeFlightFilter
from src.model.composing.filter.impl.edge_visited_global import VisitedGlobalEdgeFlightFilter
from src.model.composing.filter.impl.esoteric.price_stupid import StupidPriceFlightFilter
from src.model.composing.filter.impl.price import PriceFlightFilter
from src.model.composing.filter.impl.price_total import TotalPriceFlightFilter
from src.model.composing.filter.impl.timeout import TimeoutFlightFilter
from src.model.composing.ucs import UCSComposer
from src.model.requesting.configuration.configuration_requester import RequesterConfiguration
from src.util.browser import BrowserUtil
from src.util.gmail_api import GmailAPIUtil
from src.util.graphutil import GraphUtil
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

MAX_UCS_SEARCH_TIME_PER_PERIOD = 120
MAX_DFS_SEARCH_TIME_PER_PERIOD = 255 * 3
MAX_DFS_SEARCH_TIME_PER_INSTANCE = 30
MIN_DFS_SEARCH_TIME_PER_INSTANCE = 15

MIN_MERGING_COUNT = 10
MAX_MERGING_CC = 1300
# MIN_MERGING = [
#     {"count": 10, "cc": 1200},
#     {"count": 8, "cc": 900}
# ]

CHECK_ONLY_BIGGEST = False
GRAPH_MERGING_ACTIVATED = True
DRAWING_ACTIVATED = True


def get_actual_filters(graph_global, timeout=MAX_UCS_SEARCH_TIME_PER_PERIOD):
    return [PriceFlightFilter(), StupidPriceFlightFilter(), VisitedCountryExcludeCheapFlightFilter(),
            TotalPriceFlightFilter(), TimeoutFlightFilter(timeout)]
    # VisitedEdgeFlightFilter(), TODO
    # VisitedGlobalEdgeFlightFilter(graph_global)


pretty_printer = pprint.PrettyPrinter()

instance_id = random.getrandbits(12)
Logger.debug("Started instance {}".format(instance_id))

eu_airports_list = open(PATH_DATA_EU_AIRPORTS, 'r').read().splitlines()
eu_airports = [x.split("\t") for x in eu_airports_list]

# actual for 2017-02-16 23:16
# the first 6-th are the biggest
biggest_eu_airports_list = ['BRU', 'SOF', 'BLL', 'CPH', 'CGN', 'GDN', 'VIE', 'PFO', 'OSR', 'TLS', 'FRA', 'FMM', 'ATH',
                            'SKG', 'BUD', 'DUB', 'SNN', 'BLQ', 'PSA', 'VNO', 'TGD', 'EIN', 'OSL', 'KTW', 'KRK', 'WAW',
                            'WRO', 'FAO', 'OPO', 'TSR', 'BTS', 'ALC', 'BCN', 'MAD', 'MAN']
# biggest_eu_airports_list = ['OSR']

date_period_list = [datetime(2017, 2, 23), datetime(2017, 3, 1), datetime(2017, 4, 23)]

list_big_airports = OrderedSet()

best_count_result = 0
best_cost_result = 0
best_route_result = []

graph_total = nx.MultiDiGraph()

counter = 0
figures_count = 0
counter_threads_total = 0
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

        configuration_requester = RequesterConfiguration(date_period)
        composer_ucs = DFSComposer()  # TODO
        try:
            graph = composer_ucs.find_flights(orig_iata, configuration_requester, get_actual_filters(graph_total))
            count_result, cost_result, countries_result, route_result = composer_ucs.count_result, \
                                                                        composer_ucs.cost_result, \
                                                                        composer_ucs.countries_result, \
                                                                        composer_ucs.list_flights
            GraphUtil.remove_duplicate_edges(graph)

            # if composer_ucs.queue.qsize() > 0:
            #     Logger.info("For airport {} running {} DFS tasks.".format(orig_iata, composer_ucs.queue.qsize()))
            #     time_per_dfs = max(min(round(MAX_DFS_SEARCH_TIME_PER_PERIOD / composer_ucs.queue.qsize()),
            #                            MAX_DFS_SEARCH_TIME_PER_INSTANCE),
            #                        MIN_DFS_SEARCH_TIME_PER_INSTANCE)
            #     counter_dfs_tasks = 1
            #     while not composer_ucs.queue.empty():
            #         hash_code = composer_ucs.queue.get()[1]
            #         city_orig_dfs = composer_ucs.map_routes_queue[hash_code][0]
            #         list_previous_flights = composer_ucs.map_routes_queue[hash_code][1]
            #
            #         Logger.info("Running DFS task #{} for airport {}: start from {}.".format(counter_dfs_tasks, orig_iata,
            #                                                                                  city_orig_dfs))
            #         counter_dfs_tasks += 1
            #         composer_dfs = DFSComposer()
            #         graph_dfs = composer_dfs.find_flights(city_orig_dfs, configuration_requester,
            #                                               get_actual_filters(graph_total, timeout=time_per_dfs),
            #                                               graph=graph, list_previous_flights=list_previous_flights)
            #         count_result_dfs, cost_result_dfs, countries_result_dfs, route_result_dfs = composer_dfs.count_result, \
            #                                                                                     composer_dfs.cost_result, \
            #                                                                                     composer_dfs.countries_result, \
            #                                                                                     composer_dfs.list_flights
            #         GraphUtil.merge_graphs(graph, graph_dfs)
            #
            #         if (len(countries_result_dfs) > count_result) \
            #                 | ((len(countries_result_dfs) == count_result) & (cost_result_dfs < cost_result)):
            #             count_result = len(countries_result_dfs)
            #             cost_result = cost_result_dfs
            #             countries_result = countries_result_dfs
            #             route_result = route_result_dfs

            if GRAPH_MERGING_ACTIVATED & (count_result > 0):
                if (count_result >= MIN_MERGING_COUNT) & (round(cost_result / count_result) < MAX_MERGING_CC):
                    if DRAWING_ACTIVATED:
                        figures_count += 1
                        file_name = "{}_{}_{}_{}-{}".format(instance_id, counter, datetime.strftime(date_period, "%m"),
                                                            graph.number_of_nodes(),
                                                            graph.number_of_edges())
                        GraphUtil.draw_hierarhical(graph, file_name, figures_count)
                    GraphUtil.merge_graphs(graph_total, graph)

            if (count_result >= 14) and (round(cost_result / count_result) <= 1100):
                Logger.info("Starting process to search for routes! Route description: ({}-{} at {}-{})"
                            "".format(route_result[0].orig_city, route_result[-1].dest_city,
                                      datetime.strftime(route_result[0].depart_date, DATE_FORMAT),
                                      datetime.strftime(route_result[-1].depart_date, DATE_FORMAT)))
                if __name__ == '__main__':
                    controller_start = StartDockingCallableController()
                    controller_finish = FinishDockingCallableController()
                    Thread(target=controller_start.dock(route=route_result)).start()
                    Thread(target=controller_finish.dock(route=route_result)).start()
                counter_threads_total += 1

        except ValueError as e:
            Logger.system("Caught very broad Exception. Origin: {}, period: {}, "
                          "exception message: {}".format(orig_iata, date_period, str(e)))

        if (len(countries_result) > period_count_result) \
                | ((len(countries_result) == period_count_result) & (cost_result < period_cost_result)):
            period_count_result = len(countries_result)
            period_cost_result = cost_result
            period_countries_result = countries_result
            period_route_result = route_result
        if time.time() - time_start_period > MAX_UCS_SEARCH_TIME_PER_PERIOD:
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

        # if (period_count_result >= 14) and (round(period_cost_result / period_count_result) <= 1100):
        #     controller = StartDockingCallableController()
        #     Logger.info("Starting process to search for routes! Route description: ({}-{} at {}-{})"
        #                 "".format(period_route_result[0].orig_city, period_route_result[-1].dest_city,
        #                           datetime.strftime(period_route_result[0].depart_date, DATE_FORMAT),
        #                           datetime.strftime(period_route_result[-1].depart_date, DATE_FORMAT)))
        #     process = Process(target=controller.dock(route=period_route_result))
        #     process.start()

        # cool_condition_1 = ((period_count_result >= 15) & (round(period_cost_result / period_count_result) <= 1000))
        # cool_condition_2 = ((period_count_result > 10) & (round(period_cost_result / period_count_result) <= 500))
        # if cool_condition_1 | cool_condition_2:
        #     cool_status = "AMAZINGLY COOL" if cool_condition_1 else "pretty cool"
        #
        #     links_list = []
        #     for flight in period_route_result:
        #         links_list.append(BrowserUtil.create_link(flight))
        #     links_message = "\n".join(links_list)
        #
        #     subject = "[TripMaker] {} route: {} countries, " \
        #               "{} rub ({} r/c)".format(cool_status, period_count_result, period_cost_result,
        #                                        round(period_cost_result / period_count_result))
        #
        #     start_point = "{} ({}, {})".format(*airport)
        #     finish_point = period_route_result[-1].dest_city
        #
        #     body = body_route.format(count_countries=period_count_result, price=period_cost_result,
        #                              cc=round(period_cost_result / period_count_result),
        #                              start_point=start_point, finish_point=finish_point,
        #                              countries_visited=period_countries_result, cool_status=cool_status,
        #                              dump=period_route_result.to_json(), links=links_message)
        #     message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)
        #
        #     GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
        #     Logger.error("Sending: {}".format(subject))
    else:
        Logger.info("Nothing found for {} ({}, {})".format(*airport))

    Logger.info("")

    if (len(countries_result) > best_count_result) \
            | ((len(countries_result) == best_count_result) & (cost_result < best_cost_result)):
        best_count_result = len(countries_result)
        best_cost_result = cost_result
        best_countries_result = countries_result
        best_route_result = route_result

GraphUtil.draw_hierarhical(graph_total, "{}_total_{}-{}".format(instance_id, graph_total.number_of_nodes(),
                                                                graph_total.number_of_edges()), figures_count + 1)

message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com",
                                      "[TripMaker] Computations completed",
                                      "I finished. Restart me! Also, {} threads was running.".format(
                                          counter_threads_total))
GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)

Logger.info("List of big airports ({}): {}".format(len(list_big_airports), list_big_airports))

# Logger.info("Best total result: visited {} countries for {} rub: {}".format(best_count_result,
#                                                                             best_cost_result, best_countries_result))
# Logger.info("The route:")
# Logger.info(route_result.to_json())
