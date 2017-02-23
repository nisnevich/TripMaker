from datetime import datetime, timedelta

import networkx as nx
import sys

from src.entity.flight import Flight
from src.util.graphsearch import single_source_dijkstra

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
f.price = 500
G.add_edge("KJA", "LED", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 4)
f.price = 1000
G.add_edge("LED", "MOW", flight=f)

f = Flight()
f.depart_date = datetime(2017, 3, 3)
f.price = 1000
G.add_edge("LED", "BER", flight=f)


def get_weight(a, b, data, **kwargs):
    edges_in = G.in_edges(a)

    if len(edges_in) == 0:
        # One out edge
        if len(data) == 1:
            return data[0]["flight"].price
        # Multi out edges -> add each to visit later
        else:
            for edge_out in data: # TODO test
                price = edge_out["flight"] + kwargs["cost"]
                kwargs["push"](kwargs["fringe"], (price, next(kwargs["counter"]), b))
            return None # TODO check if it is correct to return None in this case

    if len(data) == 1:
        flight = data[0]["flight"]
        min_price = sys.maxsize
        for edge in edges_in:
            date_from = edge["flight"].depart_date + timedelta(days=1)
            date_to = edge["flight"].depart_date + timedelta(days=7)
            if date_from <= flight.depart_date <= date_to:
                if min_price > flight.price:
                    min_price = flight.price
        if min_price != sys.maxsize:
            return min_price
        return None
    else:
        for edge_out in data: # TODO test
            price = edge_out["flight"] + kwargs["cost"]
            kwargs["push"](kwargs["fringe"], (price, next(kwargs["counter"]), b))
        return None # TODO check if it is correct to return None in this case

print(single_source_dijkstra(G, "KJA", "MOW", get_weight=get_weight))
