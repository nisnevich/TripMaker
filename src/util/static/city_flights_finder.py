from datetime import datetime

from src.model.requesting.requester.asl.latest_prices import get_lowest_prices_flights_list

list_dest = ["MOW", "LED", "HEL", "TLL", "RIX", "MSQ", "IEV", "ROV", "KRR"]

city_origin = "LUX"
date_from = datetime(2017, 5, 10)
date_to = datetime(2017, 5, 30)

flights = get_lowest_prices_flights_list(city_origin, date_from, date_to)

for f in flights:
    print(f.to_json)
