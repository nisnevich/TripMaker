import random
from queue import PriorityQueue

import networkx as nx

from src.entity.flightroute import FlightsRoute
from src.model.requesting.service_requester import RequesterService
from src.util.country import CountryUtil
from src.util.log import Logger
from src.util.orderedset import OrderedSet


class UCSComposer:
    count_result = 0
    cost_result = 0
    countries_result = {}
    list_flights = []
    queue = None
    map_routes_queue = None

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

    def find_flights(self, city_orig, config_requester, list_filters=[]):
        graph = nx.MultiDiGraph()
        list_previous_flights = FlightsRoute()
        self.map_routes_queue = {}
        self.queue = PriorityQueue()

        hash_code = random.getrandbits(128)
        self.queue.put((0, hash_code))
        self.map_routes_queue[hash_code] = (city_orig, FlightsRoute())

        while not self.queue.empty():
            hash_code = self.queue.get()[1]
            city_orig = self.map_routes_queue[hash_code][0]

            if graph.number_of_nodes() == 0:
                list_flights = RequesterService.get_flights_map(city_orig, config_requester)
            else:
                list_previous_flights = self.map_routes_queue[hash_code][1]
                del self.map_routes_queue[hash_code]
                list_flights = RequesterService.get_flights_map(city_orig, config_requester,
                                                                list_previous_flights[-1].depart_date)
            country_orig = CountryUtil.get_country(city_orig)
            if city_orig not in graph.node:
                graph.add_node(city_orig, country=country_orig)

            is_finish = True
            for flight in list_flights:
                try:
                    flight.orig_country = country_orig
                    flight.dest_country = CountryUtil.get_country(flight.dest_city)
                except ValueError as e:
                    Logger.debug("[IGNORE:NOT_FOUND] " + str(e))
                    continue

                if not self.filter_continue(flight, list_previous_flights, graph, list_filters):
                    continue
                if not self.filter_break(flight, list_previous_flights, graph, list_filters):
                    break
                if not self.filter_return(flight, list_previous_flights, graph, list_filters):
                    return graph

                is_finish = False
                Logger.info(
                    "Flying from {} ({}) to {} ({}) for {} rub at {}!".format(flight.orig_city, flight.orig_country,
                                                                              flight.dest_city, flight.dest_country,
                                                                              flight.price, flight.depart_date))
                graph.add_edge(city_orig, flight.dest_city, flight=flight)
                list_previous_flights_copy = FlightsRoute(*list_previous_flights, flight)

                hash_code = random.getrandbits(128)
                self.queue.put((0, hash_code))
                self.map_routes_queue[hash_code] = (flight.dest_city, list_previous_flights_copy)

            if is_finish:
                countries_visited, total_cost = self.get_statistics(list_previous_flights)

                if total_cost > 0:
                    Logger.info("[COMPLETED] Count: {}, c/c: {}, cost: {}, "
                                "visited: {}".format(len(countries_visited), round(total_cost / len(countries_visited)),
                                                     total_cost, countries_visited))
                    Logger.info("The route:")
                    Logger.info(list_previous_flights.to_json(), is_route=True)
                else:
                    Logger.info("[COMPLETED] Nothing found")

                if (len(countries_visited) > self.count_result) \
                        | ((len(countries_visited) == self.count_result) & (total_cost < self.cost_result)):
                    self.count_result = len(countries_visited)
                    self.cost_result = total_cost
                    self.countries_result = countries_visited
                    self.list_flights = list_previous_flights

        return graph

    def get_statistics(self, list_flights):
        countries_visited = OrderedSet()
        total_cost = 0
        for f in list_flights:
            countries_visited.add(f.orig_country)
            countries_visited.add(f.dest_country)
            total_cost += f.price
        return countries_visited, total_cost
