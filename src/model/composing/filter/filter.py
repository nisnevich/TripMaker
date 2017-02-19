from abc import ABCMeta, abstractmethod


class GeneratorFilter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do_filter(self):
        pass
