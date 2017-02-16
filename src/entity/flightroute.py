import json
from datetime import datetime

from src.const.constants import DATE_FORMAT
from src.entity.flight import Flight


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
