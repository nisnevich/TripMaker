# ----- System imports

# ----- Local imports
from datetime import datetime

import networkx as nx
from jsonpickle import json

from src.const.constants import DATE_FORMAT, PATH_ROUTE_DUMP
from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.impl.country_visited_exclude_cheap import VisitedCountryExcludeCheapFlightFilter
from src.model.composing.filter.impl.price_total import TotalPriceFlightFilter
from src.model.composing.filter.impl.route_docking import DockingRouteFlightFilter
from src.model.composing.ucs import UCSComposer
from src.model.requesting.configuration.configuration_requester import RequesterConfiguration
from src.util.graphutil import GraphUtil
from src.util.log import Logger
from src.util.log_analyser import LogAnalyseUtil

Logger.crunch_logs("ru_scanner.log")

LOGS_MAX_CC = 1000
LOGS_MIN_COUNTRIES_COUNT = 15
MAX_PRICE_TOTAL = 6000
date_period_list = [datetime(2017, 2, 24), datetime(2017, 3, 23), datetime(2017, 4, 23)]

cheap_tip = ["BTS", "MUC", "MIL", "SKG", "NTE", "TLS", "MSQ"]
# list_cities_origin = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ"]
list_cities_origin = ["MOW"]

# logfile_names_list = ["main_test5_full.log", "main_test6_full (dfs only).log"]
# routes = LogAnalyseUtil.get_routes(*logfile_names_list, min_countries_count=LOGS_MIN_COUNTRIES_COUNT,
#                                    max_cc=LOGS_MAX_CC)

dump = open(PATH_ROUTE_DUMP, 'r').read()
route = FlightsRoute.from_json(json.loads(dump))
routes = [route]

Logger.info("Mapping:")
for route in routes:
    price = route.get_price_total()
    count = len(route.get_countries_visited())
    Logger.info("Mapping route: ({}-{} at {}-{}), {} countries, {} rub, c/c={} rub"
                "".format(route[0].orig_city, route[-1].dest_city,
                          datetime.strftime(route[0].depart_date, DATE_FORMAT),
                          datetime.strftime(route[-1].depart_date, DATE_FORMAT),
                          count, price, round(price / count)))
    Logger.debug(route.to_json())


# TODO add edge_visited filter
filter_total_price = TotalPriceFlightFilter()
filter_total_price.max_total_price = MAX_PRICE_TOTAL
list_filters = [DockingRouteFlightFilter(routes),
                VisitedCountryExcludeCheapFlightFilter(),
                filter_total_price]

graph_total = nx.MultiDiGraph()
counter = 1
for city_origin in list_cities_origin:
    Logger.error("#{}) Selected airport: {}".format(counter, city_origin))
    for date_period in date_period_list:
        Logger.info("For airport {} selected period: {}".format(city_origin, date_period))
        configuration_requester = RequesterConfiguration(date_period)
        graph = UCSComposer().find_flights(city_origin, configuration_requester, list_filters)
        GraphUtil.remove_duplicate_edges(graph)
        GraphUtil.merge_graphs(graph_total, graph)
    counter += 1
GraphUtil.draw_hierarhical(graph_total, "ru_total_{}-{}".format(graph_total.number_of_nodes(),
                                                                graph_total.number_of_edges()), 0)
