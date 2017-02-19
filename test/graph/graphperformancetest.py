import random
import string

import networkx as nx
import matplotlib.pyplot as plt
import time

from src.entity.flight import Flight

LENGTH_KEY = 3
COUNT_OF_NODES = 4000

s = []
start = time.time()
for i in range(0, COUNT_OF_NODES):
    s.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(LENGTH_KEY)))
print("Strings generating took {} sec".format(time.time() - start))

G = nx.MultiDiGraph()
start = time.time()
for i in range(0, COUNT_OF_NODES):
    G.add_node(s[i])

for node_from in G.nodes():
    for node_to in G.nodes():
        G.add_edge(node_from, node_to, date="03-02-2017")
print("Graph generating took {} sec".format(time.time() - start))

# start = time.time()
# for node in G.nodes():
#     neighbor = G.neighbors(node)
#     for nei in neighbor:
#         a = nei
# print("Graph accessing by nodes took {} sec".format(time.time() - start))

start = time.time()
for node in G.nodes():
    mynode = G.node[node]
    for neighbor in mynode:
        a = neighbor
print("Graph accessing by index took {} sec".format(time.time() - start))

# start = time.time()
# for edge in G.edges():
#     a = edge
# print("Graph accessing by G.edges() took {} sec".format(time.time() - start))
#
# start = time.time()
# G.edges()
# print("Graph edges extraction took {} sec".format(time.time() - start))

# plt.axis('off')
# plt.show()
