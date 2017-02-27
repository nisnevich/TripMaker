from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class VisitedGlobalEdgeFlightFilter(FlightFilter):
    def __init__(self, graph_global):
        super().__init__()
        self.graph_global = graph_global

    # TODO does this filter do the same as edge_visited? Inheritance may be useful
    def filter_continue(self, flight, list_flights, graph):
        if flight.orig_city in self.graph_global:
            if flight.dest_city in self.graph_global[flight.orig_city]:
                for edge_index in self.graph_global[flight.orig_city][flight.dest_city]:
                    flight = self.graph_global[flight.orig_city][flight.dest_city][edge_index]["flight"]
                    if flight.depart_date == flight.depart_date:
                        if flight.price > flight.price:
                            flight.price = flight.price
                        Logger.debug(("[IGNORE:EDGE_VISITED_GLOBAL] Ignore flight from {} ({})"
                                      " to {} ({}) (for {} rub): such edge is already presented in global graph!"
                                      "").format(flight.orig_city, flight.orig_country, flight.dest_city,
                                                 flight.orig_country, flight.price, flight.dest_country))
                        return False
        return True
