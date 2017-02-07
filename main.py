import json
import requests


class TripMaker(object):
    result_count = 0
    result_cost = 0
    result_route = []
    world_cities_list = []

    def __init__(self):
        with open('data/world_cities.json', encoding="utf8") as data_file:
            self.world_cities_list = json.load(data_file)

        self.find_lowest_price("MOW", [self.get_country("MOW")], 0)

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

    @staticmethod
    def lowest_prices_list(origin_iata):
        prices = requests.get(("http://map.aviasales.ru/prices.json?origin_iata={origin_iata}&period=year&one_way=true"
                               ).format(origin_iata=origin_iata)).json()
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

    def find_lowest_price(self, iata_origin, iata_visited_list, total_cost):
        low_prices_list = self.lowest_prices_list(iata_origin)

        for flight in low_prices_list:
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

            if flight["value"] > 3000:
                # print("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): too expensive!".format(
                #     flight["origin"], flight["destination"], flight["value"]))
                break

            if flight["value"] + total_cost < 20000:
                print("Flying to {} ({}) for {} rub!".format(flight["destination"], country_dest, flight["value"]))

                visited_list = list(iata_visited_list)
                visited_list.append(country_dest)
                self.find_lowest_price(flight["destination"], visited_list, flight["value"] + total_cost)
            else:
                print("[COMPLETED] Count: {}, cost: {} ".format(len(iata_visited_list), total_cost), iata_visited_list)
                if (len(iata_visited_list) > self.result_count) \
                        | (len(iata_visited_list) == self.result_count) & (total_cost < self.result_cost):
                    self.result_count = len(iata_visited_list)
                    self.result_cost = total_cost
                    self.result_route = iata_visited_list

TripMaker()
# 'RU', 'BY', 'LT', 'SE', 'PL', 'GB', 'IE', 'BE', 'RO', 'DE', 'IT', 'BG', 'GR', 'MT', 'ES', 'FR', 'PT', 'NL'
# 'RU', 'BY', 'LT', 'SE', 'PL', 'GB', 'IE', 'BE', 'RO', 'DE', 'IT', 'NL', 'RS', 'SK', 'ES', 'MT', 'GR', 'BG', 'GE', 'CY'
