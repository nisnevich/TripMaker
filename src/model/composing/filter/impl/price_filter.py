import time

from src.model.composing.filter.filter import GeneratorFilter
from src.util.log import Logger


class PriceGeneratorFilter(GeneratorFilter):
    time_start = 0
    timeout = 0

    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def do_filter(self, graph_city, node_city):

        if (flight.orig_country == "RU") | (flight.dest_country == "RU"):
            if flight.price > MAX_BILL_PRICE_RU:
                Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                              "too expensive for Russia!").format(flight.orig_city, flight.dest_city, flight.price))
                break
        elif CountryUtil.is_airport_european(flight.orig_city):
            if flight.price > MAX_BILL_PRICE_EU:
                Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                              "too expensive for Europe!").format(flight.orig_city, flight.dest_city, flight.price))
                break
        elif flight.price > MAX_BILL_PRICE_GENERIC:
            Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                          "too expensive!").format(flight.orig_city, flight.dest_city, flight.price))
            break
        return True
