# ----- System imports
import json
import pprint
from datetime import datetime, timedelta
from enum import Enum

# ----- Third-party imports
import requests

# ----- Functional constants

# Главные (крупнейшие + наиболее близкие к Европе): MOW - Мск, LED - СПб
# Второстепенные: KGD - Калининград, PKV - Псков, BZK - Брянск, EGO - Белгород, PES - Петрозаводск, VOZ - Воронеж,
# VOG - Волгоград, ROV - Ростов, AER - Сочи, MCX - Махачкала, RTW - Саратов, KUF - Самара, KZN - Казань,
# GOJ - Нижний Новгород
DEFAULT_ORIGIN_IATA = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ", "VOG", "ROV", "AER", "MCX", "RTW", "KUF",
                       "KZN", "GOJ"]
MAX_TOTAL_PRICE = 20000
MAX_BILL_PRICE_RU = 4000
MAX_BILL_PRICE_EU = 4000
MAX_BILL_PRICE_INSIDE_COUNTRY = 500
MAX_BILL_PRICE_GENERIC = MAX_BILL_PRICE_RU
ORIGIN_DATE_PERIOD = "2017-02-11:month"
MIN_DAYS_PER_COUNTRY = 1
MAX_DAYS_PER_COUNTRY = 7
DATE_FORMAT = "%Y-%m-%d"

# ----- Application constants

PATH_DATA_WORLD_CITIES = '../data/world_cities.json'
PATH_DATA_EU_AIRPORTS = '../data/eu_airports.data'


# ----- Entities

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


class TripMaker(object):
    count_result = 0
    cost_result = 0
    countries_result = {}
    route_result = []
    world_cities_list = []
    eu_airports_list = []
    pretty_printer = pprint.PrettyPrinter()

    def __init__(self, list_orig_cities_iata):
        with open(PATH_DATA_WORLD_CITIES, encoding="utf8") as data_file:
            self.world_cities_list = json.load(data_file)
        eu_airports = open(PATH_DATA_EU_AIRPORTS, 'r').read().splitlines()
        self.eu_airports = [x.split("\t") for x in eu_airports]

        for orig_iata in list_orig_cities_iata:
            list_flights = self.get_lowest_prices_flights_list(orig_iata)
            self.filter_flights(list_flights, {self.get_country(orig_iata)})

        print("Best result: visited {} countries for {} rub: {}".format(self.count_result,
                                                                        self.cost_result, self.countries_result))
        print("The route:")
        self.pretty_printer.pprint([vars(obj) for obj in self.route_result])

    def get_country(self, iata):
        country = ""

        for city in self.world_cities_list:
            if city["code"] == iata:
                country = city["country_code"]
                break
        if len(country) == 0:
            raise ValueError('IATA not found in cities base: "{}"'.format(iata))
        return country

    def is_airport_european(self, iata):
        for eu_airport in self.eu_airports:
            if iata == eu_airport[0]:
                return True
        return False

    def is_same_countries(self, iata_1, iata_2):
        country_1, country_2 = "", ""

        for city in self.world_cities_list:
            if city["code"] == iata_1:
                country_1 = city["country_code"]
                if len(country_2) > 0:
                    break
            if city["code"] == iata_2:
                country_2 = city["country_code"]
                if len(country_1) > 0:
                    break
        if len(country_1) == 0:
            raise ValueError('IATA not found in cities base: "{}"'.format(iata_1))
        if len(country_2) == 0:
            raise ValueError('IATA not found in cities base: "{}"'.format(iata_2))
        return country_1 == country_2, country_1, country_2

    def get_lowest_prices_flights_list(self, orig_iata, date_from=None, date_to=None):
        if date_from is None:
            period = ORIGIN_DATE_PERIOD
        else:
            period = datetime.strftime(date_from, DATE_FORMAT) + ":month"

        request = ("http://map.aviasales.ru/prices.json?origin_iata={orig_iata}&period={period}"
                   "&one_way=true").format(orig_iata=orig_iata, period=period)
        flights_data = requests.get(request).json()

        flights = [Flight(f['origin'], f['destination'], datetime.strptime(f['depart_date'], DATE_FORMAT),
                          f['value']) for f in flights_data]
        if date_to is not None:
            if date_to.month - date_from.month != 0:
                flights.extend(self.get_lowest_prices_flights_list(orig_iata, date_to))
            flights_filtered = []
            # Filter dates
            for f in flights:
                if date_from <= f.depart_date <= date_to:
                    flights_filtered.append(f)
            flights = flights_filtered
        # Array may be empty
        if len(flights) > 0:
            try:
                return sorted(flights, key=lambda f: f.price, reverse=False)
            except TypeError as e:
                print("Strange thing happened. len(flights)={}, flights={}".format(len(flights), flights))
                print(str(e))
                return []
        else:
            return []

    def get_flights(self, list_flights_route, countries_visited, total_cost=0):
        flight_last = list_flights_route[-1]

        date_from = flight_last.depart_date + timedelta(days=MIN_DAYS_PER_COUNTRY)
        date_to = flight_last.depart_date + timedelta(days=MAX_DAYS_PER_COUNTRY)
        list_flights = self.get_lowest_prices_flights_list(flight_last.dest_city,
                                                           date_from, date_to)
        self.filter_flights(list_flights, countries_visited, list_flights_route, total_cost)

    def filter_flights(self, list_flights, countries_visited, list_flights_route=[], total_cost=0):
        for flight in list_flights:
            try:
                flight.orig_country = self.get_country(flight.orig_city)
                flight.dest_country = self.get_country(flight.dest_city)
            except ValueError as e:
                print("[IGNORE:NOT_FOUND] " + str(e))
                continue

            if (flight.orig_country == "RU") | (flight.dest_country == "RU"):
                if flight.price > MAX_BILL_PRICE_RU:
                    print(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                           "too expensive for Russia!").format(flight.orig_city, flight.dest_city, flight.price))
                    break
            elif self.is_airport_european(flight.orig_city):
                if flight.price > MAX_BILL_PRICE_EU:
                    print(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                           "too expensive for Europe!").format(flight.orig_city, flight.dest_city, flight.price))
                    break
            elif flight.price > MAX_BILL_PRICE_GENERIC:
                print(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                       "too expensive!").format(flight.orig_city, flight.dest_city, flight.price))
                break
            if (flight.orig_country == flight.dest_country) & (flight.price <= MAX_BILL_PRICE_INSIDE_COUNTRY):
                print(("[ATTENTION:VISIT_INSIDE] Allowed flight from {} to {} (both in {}): "
                       "the price is {}!").format(flight.orig_city, flight.dest_city,
                                                  flight.dest_country, flight.price))
            elif flight.dest_country in countries_visited:
                print(("[IGNORE:ALREADY_VISITED] Ignore flight from {} to {} (for {} rub): "
                       "{} already visited!").format(flight.orig_city, flight.dest_city, flight.price,
                                                     flight.dest_country))
                continue

            if flight.price + total_cost < MAX_TOTAL_PRICE:
                print("Flying from {} ({}) to {} ({}) for {} rub at {}!".format(flight.orig_city, flight.orig_country,
                                                                                flight.dest_city, flight.dest_country,
                                                                                flight.price, flight.depart_date))
                flights_history_extended = list(list_flights_route)
                flights_history_extended.append(flight)
                countries_visited_extended = set(countries_visited)
                countries_visited_extended.add(flight.dest_country)
                cost = flight.price + total_cost

                self.get_flights(flights_history_extended, countries_visited_extended, cost)
            else:
                break

        print("[COMPLETED] Count: {}, cost: {}, visited: {}".format(len(countries_visited),
                                                                    total_cost, countries_visited))
        if (len(countries_visited) > self.count_result) \
                | ((len(countries_visited) == self.count_result) & (total_cost < self.cost_result)):
            self.count_result = len(countries_visited)
            self.cost_result = total_cost
            self.countries_result = countries_visited
            self.route_result = list_flights_route


TripMaker(DEFAULT_ORIGIN_IATA)
