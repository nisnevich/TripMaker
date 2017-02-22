import time

from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.country import CountryUtil
from src.util.log import Logger

STUPID_PRICE_TRESHOLD = 500


class StupidPriceFlightFilter(FlightFilter):
    def filter_continue(self, flight, list_flights, graph):
        if (flight.orig_city == "MOW") & (flight.dest_country != "RU") & (flight.price <= STUPID_PRICE_TRESHOLD):
            Logger.debug(("[IGNORE:STUPID_PRICE] Ignoring flight from {} ({}) to {} ({}) (for {} rub): "
                          "stupid price, isn't it?").format(flight.orig_city, flight.orig_country, flight.dest_city,
                                                            flight.dest_country, flight.price))
            return False
        return True
