from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class VisitedEdgeFlightFilter(FlightFilter):
    def filter_continue(self, flight, list_flights, graph):
        if flight.orig_city in graph:
            if flight.dest_city in graph[flight.orig_city]:
                for edge_index in graph[flight.orig_city][flight.dest_city]:
                    flight = graph[flight.orig_city][flight.dest_city][edge_index]["flight"]
                    if flight.depart_date == flight.depart_date:
                        if flight.price > flight.price:
                            flight.price = flight.price
                        Logger.debug(("[IGNORE:EDGE_VISITED] Ignore flight from {} ({})"
                                      " to {} ({}) (for {} rub): such edge is already presented in graph!"
                                      "").format(flight.orig_city, flight.orig_country, flight.dest_city,
                                                 flight.orig_country, flight.price, flight.dest_country))
                        return False
        return True
