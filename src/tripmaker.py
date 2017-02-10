# ----- System imports
import json
import pprint
from datetime import timedelta
import time

# ----- Local imports
from src.const.constants import *
from src.model.search.asl.latest_prices import get_lowest_prices_flights_list
from src.util.logging import Logger


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
            start_time = time.time()
            list_flights = get_lowest_prices_flights_list(orig_iata)
            Logger.info(("Flights searching from {} for a '{}' period "
                         "took {} seconds").format(orig_iata, ORIGIN_DATE_PERIOD, round(time.time() - start_time, 1)))
            self.filter_flights(list_flights, {self.get_country(orig_iata)})

        Logger.info("Best result: visited {} countries for {} rub: {}".format(self.count_result,
                                                                              self.cost_result, self.countries_result))
        Logger.info("The route:")
        Logger.info(self.pretty_printer.pformat([vars(obj) for obj in self.route_result]))

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

    def get_flights(self, list_flights_route, countries_visited, total_cost=0):
        flight_last = list_flights_route[-1]

        date_from = flight_last.depart_date + timedelta(days=MIN_DAYS_PER_COUNTRY)
        date_to = flight_last.depart_date + timedelta(days=MAX_DAYS_PER_COUNTRY)
        list_flights = get_lowest_prices_flights_list(flight_last.dest_city,
                                                      date_from, date_to)
        try:
            self.filter_flights(list_flights, countries_visited, list_flights_route, total_cost)
        except Exception as e:
            Logger.system("Caught very broad Exception. Visited countries: {}, total cost: {}, "
                          "exception message: {}".format(countries_visited, total_cost, str(e)))
            Logger.system("The route:")
            Logger.system(self.pretty_printer.pformat([vars(obj) for obj in list_flights_route]))
            return

    def filter_flights(self, list_flights, countries_visited, list_flights_route=[], total_cost=0):
        for flight in list_flights:
            try:
                flight.orig_country = self.get_country(flight.orig_city)
                flight.dest_country = self.get_country(flight.dest_city)
            except ValueError as e:
                Logger.debug("[IGNORE:NOT_FOUND] " + str(e))
                continue

            if (flight.orig_country == "RU") | (flight.dest_country == "RU"):
                if flight.price > MAX_BILL_PRICE_RU:
                    Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                                  "too expensive for Russia!").format(flight.orig_city, flight.dest_city, flight.price))
                    break
            elif self.is_airport_european(flight.orig_city):
                if flight.price > MAX_BILL_PRICE_EU:
                    Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                                  "too expensive for Europe!").format(flight.orig_city, flight.dest_city, flight.price))
                    break
            elif flight.price > MAX_BILL_PRICE_GENERIC:
                Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                              "too expensive!").format(flight.orig_city, flight.dest_city, flight.price))
                break
            if (flight.orig_country == flight.dest_country) & (flight.price <= MAX_BILL_PRICE_INSIDE_COUNTRY):
                Logger.debug(("[ATTENTION:VISIT_INSIDE] Allowed flight from {} to {} (both in {}): "
                              "the price is {}!").format(flight.orig_city, flight.dest_city,
                                                         flight.dest_country, flight.price))
            elif flight.dest_country in countries_visited:
                Logger.debug(("[IGNORE:ALREADY_VISITED] Ignore flight from {} to {} (for {} rub): "
                              "{} already visited!").format(flight.orig_city, flight.dest_city, flight.price,
                                                            flight.dest_country))
                continue

            if flight.price + total_cost < MAX_TOTAL_PRICE:
                Logger.info(
                    "Flying from {} ({}) to {} ({}) for {} rub at {}!".format(flight.orig_city, flight.orig_country,
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

        Logger.info("[COMPLETED] Count: {}, cost: {}, visited: {}".format(len(countries_visited),
                                                                          total_cost, countries_visited))
        Logger.system("The route:")
        Logger.system(self.pretty_printer.pformat([vars(obj) for obj in list_flights_route]))

        if (len(countries_visited) > self.count_result) \
                | ((len(countries_visited) == self.count_result) & (total_cost < self.cost_result)):
            self.count_result = len(countries_visited)
            self.cost_result = total_cost
            self.countries_result = countries_visited
            self.route_result = list_flights_route


TripMaker(DEFAULT_ORIGIN_IATA)
