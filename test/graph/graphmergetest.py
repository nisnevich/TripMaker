import copy
from datetime import datetime

import networkx as nx

from src.entity.flight import Flight
from src.util.graphutil import GraphUtil

G = nx.MultiDiGraph()

f1 = Flight()
f1.depart_date = datetime(2017, 3, 20)
f1.price = 1000

f2 = Flight()
f2.depart_date = datetime(2017, 3, 20)
f2.price = 500
f2.orig_city = "BER"
f2.dest_city = "BER"

G.add_node("LED", country="RU")
G.add_node("MOW", country="RU")
G.add_node("BER", country="DE")
G.add_node("KJA", country="RU")

G.add_edge("KJA", "LED", flight=f1)
G.add_edge("KJA", "LED", flight=f1)
G.add_edge("LED", "BER", flight=f1)
G.add_edge("BER", "QWE", flight=f1)

G.add_edge("LED", "MOW", flight=f1)


G1 = nx.MultiDiGraph()

G1.add_node("LED", country="RU")
G1.add_node("MOW", country="RU")
G1.add_node("BER", country="DE")
G1.add_node("KJA", country="RU")

G1.add_edge("KJA", "LED", flight=f2)
G1.add_edge("LED", "BER", flight=f1)

G1.add_edge("LED", "MOW", flight=f1)
G1.add_edge("LED", "MOW", flight=f1)

node = "LED"
print(node)  # LED
print(G.node[node])  # {'country': 'RU'}
print(G.in_edges(node))  # [('KJA', 'LED')]
print(G.out_edges(node))  # [('LED', 'BER'), ('LED', 'MOW'), ('LED', 'MOW')]
print(G.neighbors(node))  # ['BER', 'MOW']
print(G.in_edges())  # [('LED', 'MOW'), ('LED', 'MOW'), ('LED', 'BER'), ('KJA', 'LED')]

GraphUtil.remove_duplicate_edges(G)
GraphUtil.remove_duplicate_edges(G1)

res = nx.MultiDiGraph(G)
# res.add_nodes_from(G1.nodes(data=True))
# res.add_edges_from(G1.edges(data=True, keys=False))
GraphUtil.merge_graphs(res, G1)
GraphUtil.remove_duplicate_edges(G)

for e in res.edges(data=True):
    print("{}-{} for {}".format(e[0], e[1], e[2]["flight"].price))

pos = nx.spring_layout(res)
'''
if G.has_edge(e[0], e[1]):
    for edge in G.edge[e[0]][e[1]]:
        if edge[0]["flight"].depart_date == edge[1]["flight"].depart_date
'''
nx.draw_networkx_nodes(res, pos=pos, linewidths=0.5, alpha=0.8)
nx.draw_networkx_edges(res, pos=pos, width=0.5, arrows=True)

labels_nodes = {}
for node in res.nodes():
    labels_nodes[node] = node
nx.draw_networkx_labels(res, pos, labels_nodes, font_size=12, font_color='black')

# labels_edges = {}
# for edge in G.edges():
#     labels_edges[edge] = edge
# nx.draw_networkx_edge_labels(G, pos, labels=labels_edges, font_size=12, font_color='green')

# plt.axis('off')
# plt.show()
