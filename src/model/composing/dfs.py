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

    def start(self):
        '''
            Time estimation
        '''

    def filter_flights(self,
                       # ACTUAL
                       city_orig,
                       filters,
                       callback_finish,

                       # Leveled by the graph
                       list_flights,
                       # Filtration
                       countries_visited,
                       # Leveled by the graph
                       route_flights=FlightsRoute(),
                       # Filtration
                       total_cost=0, stop_list=[], target_country=None):
        '''
            1) [if not exists] Create graph
            2) Add city to graph
            3) Log that the city was visited
            Logger.info(
                "Flying from {} ({}) to {} ({}) for {} rub at {}!".format(flight.orig_city, flight.orig_country,
                                                                          flight.dest_city, flight.dest_country,
                                                                          flight.price, flight.depart_date))
        '''
        for flight in list_flights:
            '''
                Filtration

                Check:
                1) stop_list=[],
                2) target_country=None
                etc...

                P.S.: use the graph to check price

            '''

            '''
                if filter passed successfully:

                flights_history_extended: nivelated
            '''

            self.get_flights(flight.orig_city)

        '''
            finish callback
        '''

        if total_cost > 0:
            Logger.info("[COMPLETED] Count: {}, c/c: {}, cost: {}, "
                        "visited: {}".format(len(countries_visited), round(total_cost/len(countries_visited)),
                                             total_cost, countries_visited))
            Logger.info("The route:")
            Logger.info(route_flights.to_json())
        else:
            Logger.info("[COMPLETED] Nothing found")

        '''
            this thing is generator-specific (leave as is)
        '''
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
