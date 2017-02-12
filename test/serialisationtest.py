import json

from src.const.constants import PATH_LOG
from src.entity.flight import Flight
from src.entity.flightroute import FlightsRoute
from src.model.search.asl.dto.flightadapter import ASFlightDTOAdapter

f_json = '''{
    "value": 939,
    "ttl": 1486975343,
    "trip_class": 0,
    "show_to_affiliates": false,
    "return_date": null,
    "origin": "BRU",
    "number_of_changes": 0,
    "gate": null,
    "found_at": "2017-02-11T08:42:23Z",
    "distance": 0,
    "destination": "MIL",
    "depart_date": "2017-04-13",
    "created_at": 1486802543,
    "actual": true
  }'''

flights = [Flight(ASFlightDTOAdapter(json.loads(f_json))), Flight(ASFlightDTOAdapter(json.loads(f_json)))]

route = FlightsRoute(*flights)

# print(route.to_json())
#
s = open("C:\\Users\\Arseniy\\PycharmProjects\\TripMaker\\results\\mow_16_modified", "r").read()

route = FlightsRoute.from_json(json.loads(s))

print(route.to_json())
