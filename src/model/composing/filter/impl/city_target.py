from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class CitiesTargetListFlightFilter(FlightFilter):
    cities_target_list = None
    max_flights_count_before_target = None
    max_price_total_before_target = None

    def __init__(self, cities_target_list, max_flights_count_before_target=None, max_price_total_before_target=None):
        super().__init__()
        self.cities_target_list = cities_target_list
        self.max_flights_count_before_target = max_flights_count_before_target
        self.max_price_total_before_target = max_price_total_before_target
        Logger.info("Formed cities target list. Will ignore all other cities.")
        Logger.info("The list itself (max flights: {}): {}".format(max_flights_count_before_target, cities_target_list))

    def filter_continue(self, flight, list_flights, graph):
        if flight.dest_city not in self.cities_target_list:
            if self.max_price_total_before_target and \
                            list_flights.get_price_total() > self.max_price_total_before_target:
                Logger.info(("[IGNORE:CITY_TARGET:PRICE] Ignore flight from {} ({}) to {} ({}) (for {} rub):"
                             " route total price ({} rub) is more than {} rub!"
                             "").format(flight.orig_city, flight.orig_country, flight.dest_city, flight.dest_country,
                                        flight.price, list_flights.get_price_total(),
                                        self.max_price_total_before_target))
                return False
            if self.max_flights_count_before_target and \
                            len(list_flights) > self.max_flights_count_before_target:
                Logger.info(("[IGNORE:CITY_TARGET:COUNT] Ignore flight from {} ({}) to {} ({}) (for {} rub): "
                             "count of flights ({}) is over than {}!").format(flight.orig_city, flight.orig_country,
                                                                              flight.dest_city, flight.dest_country,
                                                                              flight.price, len(list_flights),
                                                                              self.max_flights_count_before_target))
                return False
        else:
            Logger.info(("[ATTENTION:FOUND_CITY_TARGET] Make an attention to flight {} ({}) to {} ({}) (for {} rub): "
                         "city {} is presented in target list (route cost - {} rub)!"
                         "").format(flight.orig_city, flight.orig_country, flight.dest_city, flight.dest_country,
                                    flight.price, flight.dest_city, list_flights.get_price_total()))
            Logger.info(list_flights.to_json())
            return False
        return True
