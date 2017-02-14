import calendar
import json
from datetime import datetime, timedelta

import requests
import matplotlib.pyplot as plt

from src.const.constants import AS_ACCESS_TOKEN, PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flight import Flight
from src.entity.flightroute import FlightsRoute
from src.model.search.asl.dto.flightadapter import ASFlightDTOAdapter

DELTA_TIME_ALTER = 7


def get_flights_month(orig_iata, dest_iata, date_from=None, date_to=None):
    period = "month&beginning_of_period={date}".format(date=datetime.strftime(date_from.replace(day=1), DATE_FORMAT))
    # FIXME use month-matrix API instead!
    request = ("http://api.travelpayouts.com/v2/prices/latest?origin={orig_iata}&destination={dest_iata}"
               "&token={token}&one_way=true&sorting=price&currency=rub"
               "&period_type={period}").format(orig_iata=orig_iata, dest_iata=dest_iata,
                                               period=period, token=AS_ACCESS_TOKEN)
    flights_data = requests.get(request).json()["data"]
    flights = [Flight(ASFlightDTOAdapter(f)) for f in flights_data]

    if date_to is not None:
        if date_to.month - date_from.month != 0:
            flights.extend(get_flights_month(orig_iata, dest_iata, date_to))
        flights_filtered = []
        # Filter dates
        for f in flights:
            if date_from <= f.depart_date <= date_to:
                flights_filtered.append(f)
        flights = flights_filtered

    return sorted(flights, key=lambda f: f.depart_date, reverse=False)

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

for flight in route_flights:
    date_alter_from = flight.depart_date - timedelta(days=DELTA_TIME_ALTER)
    date_alter_to = flight.depart_date + timedelta(days=DELTA_TIME_ALTER)
    alternate_flights = get_flights_month(flight.orig_city, flight.dest_city, date_alter_from, date_alter_to)
    for alternate_f in alternate_flights:
        print(vars(alternate_f))
    print()
