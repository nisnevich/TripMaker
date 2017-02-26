from abc import ABCMeta


class FlightFilter:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.key_flight = "flight"
        self.max_total_price = 20000
        self.max_bill_price_ru = 2400
        self.max_bill_price_eu = 2000
        self.max_bill_price_inside_country = 100
        self.max_bill_price_generic = self.max_bill_price_ru

    def filter_info(self, flight, list_flights, graph):
        return True

    def filter_continue(self, flight, list_flights, graph):
        return True

    def filter_break(self, flight, list_flights, graph):
        return True

    def filter_return(self, flight, list_flights, graph):
        return True
