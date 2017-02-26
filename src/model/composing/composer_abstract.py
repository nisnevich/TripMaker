from abc import ABCMeta
from queue import PriorityQueue

import networkx as nx

from src.util.orderedset import OrderedSet


class AbstractComposer:
    __metaclass__ = ABCMeta

    count_result = None
    cost_result = None
    countries_result = None
    list_flights = None

    queue = None
    map_routes_queue = None
    graph = None

    def __init__(self):
        self.count_result = 0
        self.cost_result = 0
        self.countries_result = {}
        self.list_flights = []

        self.queue = PriorityQueue()
        self.map_routes_queue = {}
        self.graph = nx.MultiDiGraph()

    def filter_continue(self, flight, list_previous_flights, graph, list_filters):
        for filt in list_filters:
            filt.filter_info(flight, list_previous_flights, graph)
            if not filt.filter_continue(flight, list_previous_flights, graph):
                return False
        return True

    def filter_break(self, flight, list_previous_flights, graph, list_filters):
        for filt in list_filters:
            if not filt.filter_break(flight, list_previous_flights, graph):
                return False
        return True

    def filter_return(self, flight, list_previous_flights, graph, list_filters):
        for filt in list_filters:
            if not filt.filter_return(flight, list_previous_flights, graph):
                return False
        return True

    def get_statistics(self, list_flights):
        countries_visited = OrderedSet()
        total_cost = 0
        for f in list_flights:
            countries_visited.add(f.orig_country)
            countries_visited.add(f.dest_country)
            total_cost += f.price
        return countries_visited, total_cost
