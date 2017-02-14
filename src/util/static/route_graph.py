import calendar
import json
from datetime import datetime, timedelta

import requests
import matplotlib.pyplot as plt

from src.const.constants import AS_ACCESS_TOKEN, PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flight import Flight
from src.entity.flightroute import FlightsRoute
from src.model.search.asl.dto.flightadapter import ASFlightDTOAdapter


def get_flights_month(orig_iata, dest_iata, date_from=None):
    period = "month&beginning_of_period={date}".format(date=datetime.strftime(date_from.replace(day=1), DATE_FORMAT))

    request = ("http://api.travelpayouts.com/v2/prices/latest?origin={orig_iata}&destination={dest_iata}"
               "&token={token}&one_way=true&sorting=price&currency=rub"
               "&period_type={period}").format(orig_iata=orig_iata, dest_iata=dest_iata,
                                               period=period, token=AS_ACCESS_TOKEN)
    flights_data = requests.get(request).json()["data"]
    flights = [Flight(ASFlightDTOAdapter(f)) for f in flights_data]

    return sorted(flights, key=lambda f: f.depart_date, reverse=False)

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

date_start = route_flights[0].depart_date
date_end = route_flights[-1].depart_date
dates = [date_start, date_end]

plt.figure(1)

days_count = 0
first_date = None
for f_route in route_flights:
    month_prices = []
    for d in dates:
        flights = get_flights_month(f_route.orig_city, f_route.dest_city, d)
        f_days = [f.depart_date.day for f in flights]
        for day in calendar.monthrange(d.year, d.month):
            for f in flights:
                if day == f.depart_date.day:
                    days_count += 1
                    month_prices.append(f.price)
                    break
        if first_date is None:
            first_date = flights[0].depart_date
    print(month_prices)
    # plt.subplot(111)
    # plt.plot(month_prices, month_prices)

labels = []
for day in range(1, days_count + 1):
    labels.append(datetime.strftime(datetime(first_date.year, first_date.month, first_date.day), DATE_FORMAT))
    first_date += timedelta(days=1)
print(labels)
# plt.xticks(range(0, days_count), labels)
# plt.show()


# plt.subplot(111)
# plt.plot(range(0, 3), [100, 300, 200])
#
# print([f.depart_date for f in flights])
