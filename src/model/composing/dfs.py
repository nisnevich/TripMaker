import time
import json
import pprint
from datetime import timedelta

from src.const.constants import MIN_DAYS_PER_COUNTRY, MAX_DAYS_PER_COUNTRY, MAX_BILL_PRICE_RU, MAX_BILL_PRICE_EU, \
    MAX_BILL_PRICE_GENERIC, MAX_BILL_PRICE_INSIDE_COUNTRY, MAX_TOTAL_PRICE, ORIGIN_DATE_PERIOD
from src.entity.flightroute import FlightsRoute
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.country import CountryUtil
from src.util.log import Logger
from src.util.orderedset import OrderedSet


class DFSComposer:
    start_time = 0
    is_timing_activated = False
    timing_value = 0
    count_result = 0
    cost_result = 0
    countries_result = {}
    route_result = []

    def finish(self):
        return self.count_result, self.cost_result, self.countries_result, self.route_result

    def get_flights(self, route_flights, countries_visited, total_cost=0, stop_list=[], target_country=None):
        delta_time = time.time() - self.start_time
        if self.is_timing_activated & (delta_time > self.timing_value):
            Logger.debug("Stopping DFS as time limit ({} sec) "
                         "has exceeded ({} passed)".format(self.timing_value, delta_time))
            return self.finish()

        flight_last = route_flights[-1]

        date_from = flight_last.depart_date + timedelta(days=MIN_DAYS_PER_COUNTRY)
        date_to = flight_last.depart_date + timedelta(days=MAX_DAYS_PER_COUNTRY)
        list_flights = get_lowest_prices_flights_list(flight_last.dest_city,
                                                      date_from, date_to)
        try:
            return self.filter_flights(list_flights, countries_visited, route_flights,
                                       total_cost, stop_list, target_country)
        except Exception as e:
            Logger.system("Caught very broad Exception. Visited countries: {}, total cost: {}, "
                          "exception message: {}".format(countries_visited, total_cost, str(e)))
            Logger.system("The route:")
            Logger.system(route_flights.to_json())
            return

    def filter_flights(self, list_flights, countries_visited, route_flights=FlightsRoute(),
                       total_cost=0, stop_list=[], target_country=None):
        for flight in list_flights:
            delta_time = time.time() - self.start_time
            if self.is_timing_activated & (delta_time > self.timing_value):
                Logger.debug("Stopping DFS as time limit ({} sec) "
                             "has exceeded ({} passed)".format(self.timing_value, delta_time))
                return self.finish()

            try:
                flight.orig_country = CountryUtil.get_country(flight.orig_city)
                flight.dest_country = CountryUtil.get_country(flight.dest_city)
            except ValueError as e:
                Logger.debug("[IGNORE:NOT_FOUND] " + str(e))
                continue

            if flight.dest_country == target_country:
                Logger.info(("[ATTENTION:TARGET_COUNTRY] Make an attention on the flight from {} to {} (for {} rub): "
                              "{} is in a {}, the target country!").format(flight.orig_city, flight.dest_city,
                                                               flight.price, flight.orig_city, flight.orig_country))
                Logger.info(FlightsRoute(*route_flights, flight).to_json())

            if flight.dest_country in stop_list:
                Logger.debug(("[IGNORE:DENIED_COUNTRY] Breaking trip on the flight from {} to {} (for {} rub): "
                              "found {} in stop list!").format(flight.orig_city, flight.dest_city,
                                                               flight.price, flight.dest_country))
                Logger.info(FlightsRoute(*route_flights, flight).to_json())
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
                flights_history_extended = FlightsRoute(*route_flights)
                flights_history_extended.append(flight)
                countries_visited_extended = OrderedSet(countries_visited)
                countries_visited_extended.add(flight.dest_country)
                cost = flight.price + total_cost

                self.get_flights(flights_history_extended, countries_visited_extended, cost)
            else:
                break
        if total_cost > 0:
            Logger.info("[COMPLETED] Count: {}, c/c: {}, cost: {}, "
                        "visited: {}".format(len(countries_visited), round(total_cost/len(countries_visited)),
                                             total_cost, countries_visited))
            Logger.info("The route:")
            Logger.info(route_flights.to_json())
        else:
            Logger.info("[COMPLETED] Nothing found")

        if (len(countries_visited) > self.count_result) \
                | ((len(countries_visited) == self.count_result) & (total_cost < self.cost_result)):
            self.count_result = len(countries_visited)
            self.cost_result = total_cost
            self.countries_result = countries_visited
            self.route_result = route_flights

        return self.finish()

    def start(self, orig_iata, date_period=ORIGIN_DATE_PERIOD, is_timing_activated=False, timing_value=0):
        self.is_timing_activated = is_timing_activated
        self.timing_value = timing_value
        self.start_time = time.time()
        list_flights = get_lowest_prices_flights_list(orig_iata, None, None, date_period)
        # Logger.info(("Flights searching from {} for a '{}' period "
        #              "took {} seconds").format(orig_iata, date_period, round(time.time() - self.start_time, 1)))

        return self.filter_flights(list_flights, {CountryUtil.get_country(orig_iata)})
