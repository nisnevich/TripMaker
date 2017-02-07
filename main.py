from datetime import datetime, timedelta
import json
import requests


DEFAULT_ORIGIN_IATA = "MOW"
MAX_TOTAL_PRICE = 20000
MAX_BILL_PRICE = 4000
MIN_DAYS_PER_COUNTRY = 1
MAX_DAYS_PER_COUNTRY = 7
DATE_FORMAT = "%Y-%m-%d"


class TripMaker(object):
    result_count = 0
    result_cost = 0
    result_route = []
    world_cities_list = []

    def __init__(self):
        with open('data/world_cities.json', encoding="utf8") as data_file:
            self.world_cities_list = json.load(data_file)

        self.find_lowest_price(DEFAULT_ORIGIN_IATA, [self.get_country(DEFAULT_ORIGIN_IATA)])

        print("Best result: visited {} countries for {} rub. Route: {}".format(
            self.result_count, self.result_cost, self.result_route))

    def get_country(self, iata):
        country = ""

        for city in self.world_cities_list:
            if city["code"] == iata:
                country = city["country_code"]
                break
        if len(country) == 0:
            raise ValueError('IATA not found in cities base: "{}"'.format(iata))
        return country

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

    def get_lowest_prices_list(self, origin_iata, date_from=None, date_to=None):
        prices = []
        if date_from is None:
            period = "year"
        else:
            period = datetime.strftime(date_from, DATE_FORMAT) + ":month"
            if date_to is not None:
                if date_to.month - date_from.month != 0:
                    prices.extend(self.get_lowest_prices_list(origin_iata, date_from))

        request = ("http://map.aviasales.ru/prices.json?origin_iata={origin_iata}&period={period}"
                   "&one_way=true").format(origin_iata=origin_iata, period=period)
        prices.extend(requests.get(request).json())
        # Array may be empty
        if len(prices) > 0:
            try:
                return sorted(prices, key=lambda x: x['value'], reverse=False)
            except TypeError as e:
                print("Strange thing happened. len(prices)={}, prices={}".format(len(prices), prices))
                print(str(e))
                return []
        else:
            return []

    @staticmethod
    def filter_dates(lowest_prices_list, date_from, date_to):
        filtered_list = []
        for flight in lowest_prices_list:
            date = datetime.strptime(flight['depart_date'], DATE_FORMAT)
            if date_from <= date <= date_to:
                filtered_list.append(flight)
        return filtered_list

    def find_lowest_price(self, iata_origin, iata_visited_list, origin_date=None, total_cost=0):

        if total_cost == 0:
            lowest_prices_list = self.get_lowest_prices_list(iata_origin)
        else:
            date_from = origin_date + timedelta(days=MIN_DAYS_PER_COUNTRY)
            date_to = origin_date + timedelta(days=MAX_DAYS_PER_COUNTRY)
            unfiltered_lowest_prices_list = self.get_lowest_prices_list(iata_origin, date_from, date_to)
            lowest_prices_list = self.filter_dates(unfiltered_lowest_prices_list, date_from, date_to)

        for flight in lowest_prices_list:
            try:
                countries_are_same, country_orig, country_dest = self.is_same_countries(
                    flight["origin"], flight["destination"])
            except ValueError as e:
                print("[IGNORE:NOT_FOUND] " + str(e))
                continue

            if country_dest in iata_visited_list:
                # print("[IGNORE:ALREADY_VISITED] Ignore flight from {} to {} (for {} rub): {} already visited!".format(
                #     flight["origin"], flight["destination"], flight["value"], country_dest))
                continue

            if countries_are_same:
                # print("[IGNORE:SAME_COUNTRY] Ignore flight from {} to {} (for {} rub): same country - {}!".format(
                #     flight["origin"], flight["destination"], flight["value"], country_orig))
                continue

            if flight["value"] > MAX_BILL_PRICE:
                # print("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): too expensive!".format(
                #     flight["origin"], flight["destination"], flight["value"]))
                break

            if flight["value"] + total_cost < MAX_TOTAL_PRICE:
                print("Flying to {} ({}) for {} rub at {}!".format(flight["destination"], country_dest,
                                                                   flight["value"], flight['depart_date']))

                visited_list = list(iata_visited_list)
                visited_list.append(country_dest)
                self.find_lowest_price(flight["destination"], visited_list,
                                       datetime.strptime(flight['depart_date'], DATE_FORMAT),
                                       flight["value"] + total_cost)
            else:
                print("[COMPLETED] Count: {}, cost: {} ".format(len(iata_visited_list), total_cost), iata_visited_list)
                if (len(iata_visited_list) > self.result_count) \
                        | (len(iata_visited_list) == self.result_count) & (total_cost < self.result_cost):
                    self.result_count = len(iata_visited_list)
                    self.result_cost = total_cost
                    self.result_route = iata_visited_list
        print("Finished for {}".format(iata_visited_list))


TripMaker()
