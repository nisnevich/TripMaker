import json
from datetime import datetime

from src.const.constants import DATE_FORMAT
from src.entity.flight import Flight
from src.util.orderedset import OrderedSet


class FlightsRoute(list):

    def __init__(self, *flights):
        super().__init__(flights)

    def to_json(self):
        return json.dumps([vars(f) for f in self], sort_keys=True, indent=4,
                          default=lambda o: datetime.strftime(o, DATE_FORMAT) if isinstance(o, datetime)
                          else format(o))

    @staticmethod
    def from_json(list_flights_json):
        route = FlightsRoute()
        if isinstance(list_flights_json, list):
            for json_f in list_flights_json:
                route.append(Flight.deserialize(json.dumps(json_f), DATE_FORMAT))
        else:
            route.append(Flight.deserialize(json.dumps(list_flights_json), DATE_FORMAT))
        return route

    def get_price_total(self):
        total_price = 0
        for f in self:
            total_price += f.price
        return total_price

    def get_countries_visited(self):
        countries_visited = OrderedSet()
        for f in self:
            countries_visited.add(f.orig_country)
            countries_visited.add(f.dest_country)
        return countries_visited
