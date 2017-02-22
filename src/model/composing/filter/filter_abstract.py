from abc import ABCMeta


class FlightFilter(object):
    __metaclass__ = ABCMeta

    key_flight = "flight"
    max_total_price = 20000
    max_bill_price_ru = 2400
    max_bill_price_eu = 2000
    max_bill_price_inside_country = 100
    max_bill_price_generic = max_bill_price_ru

    def filter_info(self, flight, list_flights, graph):
        return True

    def filter_continue(self, flight, list_flights, graph):
        return True

    def filter_break(self, flight, list_flights, graph):
        return True

    def filter_return(self, flight, list_flights, graph):
        return True
