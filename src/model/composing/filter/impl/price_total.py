import time

from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.country import CountryUtil
from src.util.log import Logger


class TotalPriceFlightFilter(FlightFilter):

    def filter_break(self, flight, list_flights, graph):
        if flight.price + sum(f.price for f in list_flights) >= self.max_total_price:
            return False
        return True
