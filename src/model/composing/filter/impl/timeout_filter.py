import time

from src.model.composing.filter.filter import GeneratorFilter
from src.util.log import Logger


class TimeoutGeneratorFilter(GeneratorFilter):
    time_start = 0
    timeout = 0

    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def do_filter(self, graph, **kwargs):
        if self.time_start == 0:
            self.time_start = time.time()
        time_delta = time.time() - self.time_start

        if time_delta > self.timeout:
            Logger.debug("Stopping DFS as time limit ({} sec) "
                         "has exceeded ({} passed)".format(self.timeout, time_delta))
            return False
        return True
