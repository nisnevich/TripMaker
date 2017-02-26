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

    @staticmethod
    def get_info(iata):
        '''
            Returns information about the city by iata or None, if the IATA was not found
            Format:
            {
                "code": "SCE",
                "name": "State College",
                "coordinates": {"lon":-77.84823, "lat":40.85372},
                "time_zone": "America/New_York",
                "name_translations": {
                    "de":"State College","en":"State College","zh-CN":"大学城","tr":"State College",
                    "ru":"Стейт Колледж","it":"State College","es":"State College","fr":"State College",
                    "th":"สเตทคอลเลจ"
                },
                "country_code": "US"
            }
        :param iata:
        :return:
        '''
        for city in CountryUtil.world_cities_list:
            if city["code"] == iata:
                return city
        return None
