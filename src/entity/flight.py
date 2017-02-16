# ----- System imports
import json
from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum


class Flight(object):
    class SeatClass(Enum):
        economic = "economic"
        business = "business"

    def __init__(self, flight_dto=None):
        if flight_dto is not None:
            self.orig_city = flight_dto.get_orig_city()
            self.dest_city = flight_dto.get_dest_city()
            self.depart_date = flight_dto.get_depart_date()
            self.price = flight_dto.get_price()
            self.found_at = flight_dto.get_found_at()

    @staticmethod
    def deserialize(json_obj, date_format):
        def datetime_parser(dct):
            dct["depart_date"] = datetime.strptime(dct["depart_date"], date_format)
            return dct

        flight = Flight()
        flight.__dict__ = json.loads(json_obj, object_hook=datetime_parser)
        return flight

    def to_json(self, date_format):
        return json.dumps(self.__dict__,
                          default=lambda o: datetime.strftime(o, date_format) if isinstance(o, datetime)
                          else format(o))

    orig_city = None
    dest_city = None
    orig_country = None
    dest_country = None
    depart_date = None
    price = None
    found_at = None

    return_date = None
    trip_class = None
    number_of_transfers = None
    time_exceed_limit = None
    gate = None


class IFlightDTOAdapter:
    __metaclass__ = ABCMeta

    def __init__(self, flight_dict):
        self.__dict__ = json.loads(json.dumps(flight_dict))

    @abstractmethod
    def get_orig_city(self):
        pass

    @abstractmethod
    def get_dest_city(self):
        pass

    @abstractmethod
    def get_depart_date(self):
        pass

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_found_at(self):
        pass
