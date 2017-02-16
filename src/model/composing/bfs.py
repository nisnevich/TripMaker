import time
import json
import pprint
from queue import PriorityQueue
from datetime import timedelta

from src.const.constants import MIN_DAYS_PER_COUNTRY, MAX_DAYS_PER_COUNTRY, MAX_BILL_PRICE_RU, MAX_BILL_PRICE_EU, \
    MAX_BILL_PRICE_GENERIC, MAX_BILL_PRICE_INSIDE_COUNTRY, MAX_TOTAL_PRICE
from src.entity.flight import Flight
from src.entity.flightroute import FlightsRoute
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.country import CountryUtil
from src.util.log import Logger


class DFSComposer:

    count_result = 0
    cost_result = 0
    countries_result = {}
    route_result = []

    def get_flights(self, route_flights):
        flight_last = route_flights[-1]

        date_from = flight_last.depart_date + timedelta(days=MIN_DAYS_PER_COUNTRY)
        date_to = flight_last.depart_date + timedelta(days=MAX_DAYS_PER_COUNTRY)
        list_flights = get_lowest_prices_flights_list(flight_last.dest_city,
                                                      date_from, date_to)
        return list_flights

    def filter_flights(self, origin_iata):
        queue = PriorityQueue()
        queue.put(origin_iata)

        while not queue.empty():
            origin_iata = queue.get()
            flights_list = get_lowest_prices_flights_list(origin_iata)

            for flight in flights_list:
                try:
                    flight.orig_country = CountryUtil.get_country(flight.orig_city)
                    flight.dest_country = CountryUtil.get_country(flight.dest_city)
                except ValueError as e:
                    Logger.debug("[IGNORE:NOT_FOUND] " + str(e))
                    continue

                if (flight.orig_country == "RU") | (flight.dest_country == "RU"):
                    if flight.price > MAX_BILL_PRICE_RU:
                        Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                                      "too expensive for Russia!").format(flight.orig_city, flight.dest_city, flight.price))
                        break
                elif CountryUtil.is_airport_european(flight.orig_city):
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
                    flights_history_extended = FlightsRoute(route_flights)
                    flights_history_extended.append(flight)
                    countries_visited_extended = set(countries_visited)
                    countries_visited_extended.add(flight.dest_country)
                    cost = flight.price + total_cost

                    queue.put(flight)
                    self.get_flights(flights_history_extended)
                else:
                    break

        Logger.info("[COMPLETED] Count: {}, cost: {}, visited: {}".format(len(countries_visited),
                                                                          total_cost, countries_visited))
        Logger.info("The route:")
        Logger.info(route_flights.to_json())

        if (len(countries_visited) > self.count_result) \
                | ((len(countries_visited) == self.count_result) & (total_cost < self.cost_result)):
            self.count_result = len(countries_visited)
            self.cost_result = total_cost
            self.countries_result = countries_visited
            self.route_result = route_flights

        return self.count_result, self.cost_result, self.countries_result, self.route_result

    def start(self, orig_iata):
        flight = Flight()
        flight.dest_city = orig_iata
        flight.dest_country = CountryUtil.get_country(orig_iata)
        flight.price = 0

        return self.filter_flights(orig_iata)
