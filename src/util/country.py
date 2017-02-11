import json

from src.const.constants import PATH_DATA_WORLD_CITIES, PATH_DATA_EU_AIRPORTS


class CountryUtil:

    # Static class initialisation
    with open(PATH_DATA_WORLD_CITIES, encoding="utf8") as data_file:
        world_cities_list = json.load(data_file)
    eu_airports_list = open(PATH_DATA_EU_AIRPORTS, 'r').read().splitlines()
    eu_airports = [x.split("\t") for x in eu_airports_list]

    @staticmethod
    def get_country(iata):
        country = ""

        for city in CountryUtil.world_cities_list:
            if city["code"] == iata:
                country = city["country_code"]
                break
        if len(country) == 0:
            raise ValueError('IATA not found in cities base: "{}"'.format(iata))
        return country

    @staticmethod
    def is_airport_european(iata):
        for eu_airport in CountryUtil.eu_airports:
            if iata == eu_airport[0]:
                return True
        return False
