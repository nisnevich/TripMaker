import networkx as nx

from src.entity.flight import Flight

G = nx.MultiDiGraph()

G.add_node("LED", country="RU")
G.add_node("MOW", country="RU")
G.add_node("BER", country="DE")
G.add_node("KJA", country="RU")

G.add_edge("KJA", "LED", flight=Flight())
G.add_edge("LED", "BER", flight=Flight())

G.add_edges_from([("LED", "MOW", 1, dict(date="2017-02-25")), ("LED", "MOW", 2, dict(date="2017-02-27"))])

node = "LED"
print(node)  # LED
print(G.node[node])  # {'country': 'RU'}
print(G.in_edges(node))  # [('KJA', 'LED')]
print(G.out_edges(node))  # [('LED', 'BER'), ('LED', 'MOW'), ('LED', 'MOW')]
print(G.neighbors(node))  # ['BER', 'MOW']
print(G.in_edges())  # [('LED', 'MOW'), ('LED', 'MOW'), ('LED', 'BER'), ('KJA', 'LED')]



pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos=pos, linewidths=0.5, alpha=0.8)
nx.draw_networkx_edges(G, pos=pos, width=0.5, arrows=True)

labels_nodes = {}
for node in G.nodes():
    labels_nodes[node] = node
nx.draw_networkx_labels(G, pos, labels_nodes, font_size=12, font_color='black')

labels_edges = {}
for edge in G.edges():
    labels_edges[edge] = edge
nx.draw_networkx_edge_labels(G, pos, labels=labels_edges, font_size=12, font_color='green')

# plt.axis('off')
# plt.show()
