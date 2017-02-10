# ----- System imports
from enum import Enum


class Flight(object):
    class SeatClass(Enum):
        economic = "economic"
        business = "business"

    def __init__(self, orig_city, dest_city, depart_date, price):
        self.orig_city = orig_city
        self.dest_city = dest_city
        self.depart_date = depart_date
        self.price = price
        self.trip_class = Flight.SeatClass.economic

    orig_city = None
    dest_city = None
    orig_country = None
    dest_country = None
    depart_date = None
    price = None

    return_date = None
    trip_class = None
    number_of_transfers = None
    time_exceed_limit = None
    gate = None
