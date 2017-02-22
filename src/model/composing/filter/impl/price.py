import time

from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.country import CountryUtil
from src.util.log import Logger


class PriceFlightFilter(FlightFilter):

    def filter_break(self, flight, list_flights, graph):
        if ((flight.orig_country == "RU") | (flight.dest_country == "RU")) \
                & (flight.price > self.max_bill_price_ru):
            if flight.price > self.max_bill_price_ru:
                Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                              "too expensive for Russia!").format(flight.orig_city, flight.dest_city, flight.price))
                return False
        if CountryUtil.is_airport_european(flight.orig_city):
            if flight.price > self.max_bill_price_eu:
                Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                              "too expensive for Europe!").format(flight.orig_city, flight.dest_city, flight.price))
                return False
        if flight.price > self.max_bill_price_generic:
            Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                          "too expensive!").format(flight.orig_city, flight.dest_city, flight.price))
            return False
        return True
