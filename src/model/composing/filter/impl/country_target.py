from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class TargetCountryFlightFilter(FlightFilter):
    target_country = None

    def __init__(self, target_country):
        super().__init__()
        self.target_country = target_country

    def filter_info(self, flight, list_flights, graph):
        if flight.dest_country == self.target_country:
            Logger.info(("[ATTENTION:TARGET_COUNTRY] Make an attention on the flight from {} to {} (for {} rub): "
                         "{} is in a {}, the target country!").format(flight.orig_city, flight.dest_city,
                                                                      flight.price, flight.orig_city,
                                                                      flight.orig_country))
            Logger.info(FlightsRoute(*list_flights, flight).to_json())
