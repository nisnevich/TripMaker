from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class CountriesStopListFlightFilter(FlightFilter):
    countries_stop_list = None

    def __init__(self, countries_stop_list):
        super().__init__()
        self.countries_stop_list = countries_stop_list

    def filter_continue(self, flight, list_flights, graph):
        if flight.dest_country in self.countries_stop_list:
            Logger.debug(("[IGNORE:DENIED_COUNTRY] Breaking trip on the flight from {} to {} (for {} rub): "
                          "found {} in stop list!").format(flight.orig_city, flight.dest_city,
                                                           flight.price, flight.dest_country))
            Logger.info(FlightsRoute(*list_flights, flight).to_json())
            return False
        return True
