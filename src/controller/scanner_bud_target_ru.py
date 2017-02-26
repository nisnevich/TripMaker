# ----- System imports
import json

# ----- Local imports
import random
from queue import PriorityQueue

import networkx as nx

from src.const.constants import *
from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.impl.country_target import TargetCountryFlightFilter
from src.model.composing.filter.impl.country_visited_exclude_cheap import VisitedCountryExcludeCheapFlightFilter
from src.model.composing.filter.impl.price_total import TotalPriceFlightFilter
from src.model.composing.ucs import UCSComposer
from src.model.requesting.configuration.configuration_requester import RequesterConfiguration
from src.util.graphutil import GraphUtil
from src.util.log import Logger

Logger.crunch_logs("bud_scanner.log")

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

filter_total_price = TotalPriceFlightFilter()
filter_total_price.max_total_price = 20000 - route_flights.get_price_total()
list_filters = [TargetCountryFlightFilter("RU"),
                VisitedCountryExcludeCheapFlightFilter(),
                filter_total_price]

graph_total = nx.MultiDiGraph()
configuration_requester = RequesterConfiguration(route_flights[-1].depart_date)

Logger.error("Scanning flights from {}, visited countries: {}".format(route_flights[-1].orig_city,
                                                                      route_flights.get_countries_visited()))

ucs_composer = UCSComposer()
ucs_composer.queue = PriorityQueue()
hash_code = random.getrandbits(128)
ucs_composer.queue.put((0, hash_code))
ucs_composer.map_routes_queue[hash_code] = (route_flights[-1].orig_city, route_flights)

graph = ucs_composer.find_flights(route_flights[-1].orig_city, configuration_requester, list_filters)
GraphUtil.remove_duplicate_edges(graph)

file_graph_name = "ru_total_{}-{}".format(graph_total.number_of_nodes(), graph_total.number_of_edges())
# Logger.info("Drawing result graph to the file '{}'!".format(file_graph_name))
# GraphUtil.draw_hierarhical(graph_total, file_graph_name, 0)
