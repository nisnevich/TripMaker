from io import StringIO

import matplotlib.pyplot as plt

from src.entity.flight import Flight

import networkx as nx

# and the following code block is not needed
# but we want to see which module is used and
# if and why it fails
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import write_dot

    print("using package pygraphviz")
except ImportError:
    try:
        import pydotplus
        from networkx.drawing.nx_pydot import write_dot

        print("using package pydotplus")
    except ImportError:
        print()
        print("Both pygraphviz and pydotplus were not found ")
        print("see http://networkx.github.io/documentation"
              "/latest/reference/drawing.html for info")
        print()
        raise



G = nx.MultiDiGraph()

G.add_node("LED", country="RU")
G.add_node("MOW", country="RU")
G.add_node("BER", country="DE")
G.add_node("KJA", country="RU")
G.add_node("QWE", country="RU")

G.add_edge("KJA", "LED", flight=Flight())
G.add_edge("KJA", "LED", flight=Flight())
G.add_edge("LED", "BER", flight=Flight())

G.add_edge("LED", "MOW", flight=1)

G1 = nx.MultiDiGraph()

G1.add_node("LED", country="RU")
G1.add_node("MOW", country="RU")
G1.add_node("BER", country="DE")
G1.add_node("KJA", country="RU")

G1.add_edge("KJA", "LED", flight=Flight())
G1.add_edge("LED", "BER", flight=Flight())

G1.add_edge("LED", "MOW", flight=2)
G1.add_edge("LED", "MOW", flight=3)

node = "LED"
print(node)  # LED
print(G.node[node])  # {'country': 'RU'}
print(G.in_edges(node))  # [('KJA', 'LED')]
print(G.out_edges(node))  # [('LED', 'BER'), ('LED', 'MOW'), ('LED', 'MOW')]
print(G.neighbors(node))  # ['BER', 'MOW']
print(G.in_edges())  # [('LED', 'MOW'), ('LED', 'MOW'), ('LED', 'BER'), ('KJA', 'LED')]

res = nx.MultiDiGraph(G)
res.add_nodes_from(G1.nodes(data=True))
res.add_edges_from(G1.edges(data=True, keys=False))



for e in res.edges(data=True):
    print(e)

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

write_dot(res, "grid.dot")
pydotplus.graph_from_dot_file("grid.dot").write_png("dtree2.png")

print("Now run: neato -Tps grid.dot >grid.ps")

# plt.axis('off')
# plt.show()
