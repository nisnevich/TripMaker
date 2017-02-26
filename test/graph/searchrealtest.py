import os

import networkx as nx
from networkx.drawing.nx_pydot import read_dot

import pydotplus

from src.const.constants import PATH_LOG_GRAPHS
from src.model.searching.dijkstra import DijkstraSearcher

graph_name = "1339_20_02_48-72"
path_dot = os.path.join(PATH_LOG_GRAPHS, 'dumps_pickle/{}.png'.format(graph_name))
graph = nx.read_gpickle(path_dot)

# for node in graph.nodes():
#     res = DijkstraSearcher().get_cost_route("SOF", node, graph=graph)
#     if res == -1:
#         print("Cannot find path to {}".format(node))
#     else:
#         print(res)

print(DijkstraSearcher().get_cost_route("BUD", "KRK", graph=graph))
print(DijkstraSearcher().get_cost_route("SOF", "KRK", graph=graph))

print(DijkstraSearcher().get_cost_route("MIL", "KRK", graph=graph))
print(DijkstraSearcher().get_cost_route("PRG", "KRK", graph=graph))
print(DijkstraSearcher().get_cost_route("BER", "KRK", graph=graph))

print(DijkstraSearcher().get_cost_route("SOF", "BER", graph=graph))
print(DijkstraSearcher().get_cost_route("SOF", "PRG", graph=graph))
print(DijkstraSearcher().get_cost_route("SOF", "MIL", graph=graph))
