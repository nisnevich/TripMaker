import pprint
import json
import requests

pp = pprint.PrettyPrinter(indent=4)
with open('data/world_airports.json', encoding="utf8") as data_file:
    airports_list = json.load(data_file)


def is_same_countries(iata_1, iata_2):
    country_1, country_2 = "", ""

    for airport in airports_list:
        if airport["code"] == iata_1:
            country_1 = airport["country_code"]
            if len(country_2) > 0:
                break
        if airport["code"] == iata_2:
            country_2 = airport["country_code"]
            if len(country_1) > 0:
                break
    if len(country_1) > 0:
        raise ValueError('IATA not found in airports base: "{}"'.format(iata_1))
    if len(country_2) > 0:
        raise ValueError('IATA not found in airports base: "{}"'.format(iata_2))
    return country_1 == country_2, country_1, country_2


def lowest_prices_list(origin_iata):
    prices = requests.get(("http://map.aviasales.ru/prices.json?origin_iata={origin_iata}&period=year&one_way=true"
                           ).format(origin_iata=origin_iata))
    return prices.json()


def find_lowest_price(iata_origin, iata_visited_list, total_cost):
    low_prices_list = lowest_prices_list(iata_origin)
    iata_visited_list.append(iata_origin)

    for flight in low_prices_list:
        if flight["destination"] in iata_visited_list:
            print("[IGNORE:ALREADY_VISITED] Ignore cheap flight from {} to {} (for {} rub): {} already visited!".format(
                  flight["origin"], flight["destination"], flight["value"], flight["destination"]))
            continue

        try:
            countries_are_same, country_orig, country_dest = is_same_countries(flight["origin"], flight["destination"])
        except ValueError as e:
            print("[IGNORE:NOT_FOUND] " + str(e))
            continue

        if countries_are_same:
            print("[IGNORE:SAME_COUNTRY] Ignore cheap flight from {} to {} (for {} rub): same country - {}!".format(
                flight["origin"], flight["destination"], flight["value"], country_orig))
            continue

        print("Flying to {} ({})!".format(flight["destination"], country_dest))
        find_lowest_price(flight["destination"], iata_visited_list, flight["value"] + total_cost)

find_lowest_price("PKV", [], 0)
