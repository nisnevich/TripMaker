import time

from src.model.composing.filter.filter_abstract import FlightFilter
from src.util.log import Logger


class TimeoutFlightFilter(FlightFilter):
    time_start = 0
    timeout = 0

    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def filter_return(self, flight, list_flights, graph):
        if self.time_start == 0:
            self.time_start = time.time()
        time_delta = time.time() - self.time_start

        if time_delta > self.timeout:
            Logger.debug("Stopping search as time limit ({} sec) "
                         "has exceeded ({} passed)".format(self.timeout, time_delta))
            return False
        return True
