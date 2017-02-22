from abc import ABCMeta, abstractmethod


class AbstractPriceMapRequester:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def get_flights_map(city_origin, date_from, date_to):
        pass
