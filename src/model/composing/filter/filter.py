from abc import ABCMeta, abstractmethod


class GeneratorFilter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_filter(self, graph_city, node_city):
        pass
