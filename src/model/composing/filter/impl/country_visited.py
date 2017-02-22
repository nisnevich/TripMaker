from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class VisitedCountryFlightFilter(FlightFilter):

    def filter_continue(self, flight, list_flights, graph):
        if (flight.dest_country in self.get_visited_countries(list_flights)) \
                | (flight.orig_country == flight.dest_country):
            Logger.debug(("[IGNORE:ALREADY_VISITED] Ignore flight from {} to {} (for {} rub): "
                          "{} already visited!").format(flight.orig_city, flight.dest_city, flight.price,
                                                        flight.dest_country))
            return False
        return True

    def get_visited_countries(self, list_flights):
        countries_visited = set()
        for f in list_flights:
            countries_visited.add(f.orig_country)
            countries_visited.add(f.dest_country)
        return countries_visited
