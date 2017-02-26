from src.model.composing.filter.impl.country_visited import VisitedCountryFlightFilter
from src.util.log import Logger


class VisitedCountryExcludeCheapFlightFilter(VisitedCountryFlightFilter):

    def __init__(self):
        super().__init__()
        self.is_next_continue_enabled = True

    def filter_info(self, flight, list_flights, graph):
        if (flight.orig_country == flight.dest_country) & (flight.price <= self.max_bill_price_inside_country):
            Logger.debug(("[ATTENTION:VISIT_INSIDE] Allowed flight from {} to {} (both in {}): "
                          "the price is {}!").format(flight.orig_city, flight.dest_city,
                                                     flight.dest_country, flight.price))
            self.is_next_continue_enabled = False

    def filter_continue(self, flight, list_flights, graph):
        if self.is_next_continue_enabled:
            return super().filter_continue(flight, list_flights, graph)
        else:
            self.is_next_continue_enabled = True
            return True
