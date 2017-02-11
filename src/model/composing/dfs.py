import pprint
from datetime import timedelta

from src.const.constants import MIN_DAYS_PER_COUNTRY, MAX_DAYS_PER_COUNTRY, MAX_BILL_PRICE_RU, MAX_BILL_PRICE_EU, \
    MAX_BILL_PRICE_GENERIC, MAX_BILL_PRICE_INSIDE_COUNTRY, MAX_TOTAL_PRICE
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.country import CountryUtil
from src.util.logging import Logger


class DFSComposer:

    pretty_printer = pprint.PrettyPrinter()
    count_result = 0
    cost_result = 0
    countries_result = {}
    route_result = []

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
        Logger.info("The route:")
        Logger.info(self.pretty_printer.pformat([vars(obj) for obj in list_flights_route]))

        if (len(countries_visited) > self.count_result) \
                | ((len(countries_visited) == self.count_result) & (total_cost < self.cost_result)):
            self.count_result = len(countries_visited)
            self.cost_result = total_cost
            self.countries_result = countries_visited
            self.route_result = list_flights_route

        return self.count_result, self.cost_result, self.countries_result, self.route_result
