from datetime import datetime

import networkx as nx

from src.util.lib.graphsearch import single_source_dijkstra

g = nx.MultiDiGraph()
g.add_edge(1, 2, attr_dict={"weight": 1})

def tmp():
    pass

# single_source_dijkstra(g, 1, 2, get_weight=tmp)
