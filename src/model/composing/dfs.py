import networkx as nx

from src.entity.flightroute import FlightsRoute
from src.model.composing.composer_abstract import AbstractComposer
from src.model.requesting.service_requester import RequesterService
from src.util.country import CountryUtil
from src.util.log import Logger
from src.util.orderedset import OrderedSet


class DFSComposer(AbstractComposer):

    def find_flights(self, city_orig, config_requester, list_filters=[], graph=None,
                     list_previous_flights=FlightsRoute()):
        if graph is None:
            graph = nx.MultiDiGraph()
            list_flights = RequesterService.get_flights_map(city_orig, config_requester)
        else:
            list_flights = RequesterService.get_flights_map(city_orig, config_requester,
                                                            list_previous_flights[-1].depart_date)
        country_orig = CountryUtil.get_country(city_orig)
        graph.add_node(city_orig, country=country_orig)

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

            Logger.info(
                "Flying from {} ({}) to {} ({}) for {} rub at {}!".format(flight.orig_city, flight.orig_country,
                                                                          flight.dest_city, flight.dest_country,
                                                                          flight.price, flight.depart_date))
            graph.add_edge(city_orig, flight.dest_city, flight=flight)
            list_previous_flights_copy = FlightsRoute(*list_previous_flights, flight)
            self.find_flights(flight.dest_city, config_requester, list_filters, graph, list_previous_flights_copy)

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
