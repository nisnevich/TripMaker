import os

import networkx as nx
from networkx.drawing.nx_pydot import read_dot

import pydotplus

from src.const.constants import PATH_LOG_GRAPHS, PATH_DATA_EU_AIRPORTS, DEFAULT_ORIGIN_IATA
from src.model.searching.dijkstra import DijkstraSearcher
from src.util.lib.graphsearch import single_source_dijkstra
from src.util.log import Logger

graph_name = "1826_total_294-1520"
path_dot = os.path.join(PATH_LOG_GRAPHS, 'dumps_pickle/{}.pickle'.format(graph_name))
graph = nx.read_gpickle(path_dot)


# for node in graph.nodes():
#     res = DijkstraSearcher().get_cost_route("SOF", node, graph=graph)
#     if res == -1:
#         Logger.info("Cannot find path to {}".format(node))
#     else:
#         Logger.info(res)

def get_weight(e, e_index):
    return e[e_index]["flight"].price


eu_airports_list = open(PATH_DATA_EU_AIRPORTS, 'r').read().splitlines()
eu_airports = [[orig_iata, "", ""] for orig_iata in DEFAULT_ORIGIN_IATA] + [x.split("\t") for x in eu_airports_list]

counter = 0
for airport in eu_airports:
    counter += 1
    origin = airport[0]

    Logger.info("#{}) Selected airport: {} ({}, {})".format(counter, *airport))

    if origin not in graph:
        Logger.info("PASSING")
        continue
    
    dists, paths = single_source_dijkstra(graph, origin, get_weight=get_weight)

    for city in dists:
        flights = paths[city]
        for date in dists[city]:
            cost = dists[city][date]
            Logger.info("Route from {} to {}, min price: {}".format(origin, city, cost))

        count_max = 0
        for date in flights:
            count = 0
            for flight in flights[date]:
                count += 1
                if isinstance(flight, str):  # pass origin city
                    continue
                Logger.info("\t{}-{} ({}): for {} rub (at {})".format(flight.orig_city, flight.dest_city,
                                                                       flight.dest_country,
                                                                       flight.price, flight.depart_date))
            if count > count_max:
                count_max = count
        Logger.info("Statistics: {}-{}, price={}, count={}, cc={}".format(origin, city, cost, count_max,
                                                                     round(cost/count_max)))
        Logger.info("")
    Logger.info("")
    Logger.info("")
    Logger.info("")

# FIXME (issie at 1826_total_294-1520)
'''
Route from BUD to SOF, min price: 3319
	BUD-BRU (BE): for 823 rub (arrive at 2017-03-18 00:00:00)
	BRU-SOF (BG): for 2900 rub (arrive at 2017-03-25 00:00:00)
	BUD-BER (DE): for 2120 rub (arrive at 2017-03-26 00:00:00)
	BER-SOF (BG): for 1199 rub (arrive at 2017-03-29 00:00:00)
'''

# Logger.info(DijkstraSearcher().get_cost_route("BUD", "KRK", graph=graph))
# Logger.info(DijkstraSearcher().get_cost_route("SOF", "KRK", graph=graph))
#
# Logger.info(DijkstraSearcher().get_cost_route("MIL", "KRK", graph=graph))
# Logger.info(DijkstraSearcher().get_cost_route("PRG", "KRK", graph=graph))
# Logger.info(DijkstraSearcher().get_cost_route("BER", "KRK", graph=graph))
#
# Logger.info(DijkstraSearcher().get_cost_route("SOF", "BER", graph=graph))
# Logger.info(DijkstraSearcher().get_cost_route("SOF", "PRG", graph=graph))
# Logger.info(DijkstraSearcher().get_cost_route("SOF", "MIL", graph=graph))
