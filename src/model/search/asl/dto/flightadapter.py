from datetime import datetime

from src.const.constants import DATE_FORMAT
from src.entity.flight import FlightDTOAdapter


class ASFlightDTOAdapter(FlightDTOAdapter):
    origin = None
    destination = None
    depart_date = None
    value = None

    def get_orig_city(self):
        return self.origin

    def get_dest_city(self):
        return self.destination

    def get_depart_date(self):
        return datetime.strptime(self.depart_date, DATE_FORMAT)

    def get_price(self):
        return self.value

    def __init__(self, flight_dict):
        super().__init__(flight_dict)
