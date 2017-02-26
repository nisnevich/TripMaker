import time

from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.country import CountryUtil
from src.util.log import Logger


class TotalPriceFlightFilter(FlightFilter):
    def filter_break(self, flight, list_flights, graph):
        price_total = flight.price + sum(f.price for f in list_flights)
        if price_total >= self.max_total_price:
            Logger.debug(("[IGNORE:MAX_PRICE] Breaking trip on the flight from {} to {} (for {} rub) - "
                          "max cost: {} >= {}").format(flight.orig_city, flight.dest_city, flight.price,
                                                       price_total, self.max_total_price))
            return False
        return True
