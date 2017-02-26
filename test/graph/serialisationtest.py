import os
from datetime import datetime

import networkx as nx

from src.const.constants import PATH_LOG_GRAPHS
from src.entity.flight import Flight

G = nx.MultiDiGraph()

G.add_node("LED", country="RU")
G.add_node("MOW", country="RU")
G.add_node("BER", country="DE")
G.add_node("KJA", country="RU")

f = Flight()
f.depart_date = datetime(2017, 3, 1)
f.price = 500
G.add_edge("KJA", "LED", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 1)
f.price = 1000
G.add_edge("KJA", "LED", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 1)
f.price = 300
G.add_edge("KJA", "MOW", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 4)
f.price = 1500
G.add_edge("LED", "MOW", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 4)
f.price = 100
G.add_edge("MOW", "LED", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 5)
f.price = 2000
G.add_edge("LED", "BER", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 8)
f.price = 500
G.add_edge("BER", "MOW", flight=f)

path = os.path.join(PATH_LOG_GRAPHS, 'pickle')
# nx.write_gpickle(G, path)

graph = nx.read_gpickle(path)

print(path)