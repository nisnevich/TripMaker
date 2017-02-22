import calendar
import json
from datetime import datetime, timedelta

import requests
import matplotlib.pyplot as plt

from src.const.constants import AS_ACCESS_TOKEN, PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flight import Flight
from src.entity.flightroute import FlightsRoute
from src.model.requesting.asl.dto.flightadapter import ASFlightDTOAdapter

DELTA_TIME_ALTER = 7
DATE_FORMAT_NO_DAY = "%Y-%m"


def get_flights_cheapest(orig_iata, dest_iata, date_from=None, date_to=None):
    period = "month&beginning_of_period={date}".format(date=datetime.strftime(date_from.replace(day=1),
                                                                              DATE_FORMAT))
    request = ("http://api.travelpayouts.com/v2/prices/latest?origin={orig_iata}&destination={dest_iata}"
               "&token={token}&one_way=true&sorting=price&currency=rub&limit=1000"
               "&period_type={period}").format(orig_iata=orig_iata, dest_iata=dest_iata,
                                               period=period, token=AS_ACCESS_TOKEN)
    flights_data = requests.get(request).json()["data"]
    flights = [Flight(ASFlightDTOAdapter(f)) for f in flights_data]
    flights_map = {}
    for f in flights:
        if f.depart_date in flights_map:
            if f.price < flights_map[f.depart_date].price:
                flights_map[f.depart_date] = f
        else:
            flights_map[f.depart_date] = f

    if date_to is not None:
        if date_to.month - date_from.month != 0:
            flights.extend(get_flights_cheapest(orig_iata, dest_iata, date_to))
        flights_filtered = []
        # Filter dates
        for f in flights:
            if date_from <= f.depart_date <= date_to:
                flights_filtered.append(f)
        flights = flights_filtered

    # return flights
    return sorted(flights, key=lambda f: f.depart_date, reverse=False)


dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

for flight in route_flights:
    date_alter_from = flight.depart_date - timedelta(days=DELTA_TIME_ALTER)
    date_alter_to = flight.depart_date + timedelta(days=DELTA_TIME_ALTER)
    alternate_flights = get_flights_cheapest(flight.orig_city, flight.dest_city, date_alter_from, date_alter_to)
    for alternate_f in alternate_flights:
        print(vars(alternate_f))
    print()
