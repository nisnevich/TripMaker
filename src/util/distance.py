import json
import math

from src.const.constants import PATH_DATA_WORLD_CITIES
from src.util.log import Logger


class DistanceUtil(object):

    # Static class initialisation
    world_cities = {}
    with open(PATH_DATA_WORLD_CITIES, encoding="utf8") as data_file:
        world_cities_list = json.load(data_file)
    for city in world_cities_list:
        world_cities[city["code"]] = city

    # Returns distance between cities provided by IATA codes (in km) and the start azimuth
    # Returns -1, if coordinates data is not available
    @staticmethod
    def get_city_distance(iata1, iata2):

        if iata1 == iata2:
            return 0, 0
        try:
            city1 = DistanceUtil.world_cities[iata1]
            city2 = DistanceUtil.world_cities[iata2]
        except KeyError as e:
            raise ValueError("Cannot find city by iata {} in the database ('{}'). "
                             "Iata1: {}, iata2: {}".format(str(e),PATH_DATA_WORLD_CITIES, iata1, iata2))
        coords1 = city1["coordinates"]
        coords2 = city2["coordinates"]
        if (coords1 is None) | (coords2 is None):
            return -1
        try:
            return DistanceUtil.get_distance(coords1["lat"], coords1["lon"], coords2["lat"], coords2["lon"])
        except ZeroDivisionError as e:
            # In case of emergency (to save the runtime, if wrong coordinates appear in the storage)
            Logger.error("Division by zero ({}). Iata1: {} ({}), iata2: {} ({})".format(e, iata1, coords1, iata2, coords2))
            return -1

    # Returns the distance between two points (in km) and the start azimuth
    # Uses the haversine formula with a modification to the antipodes (implementation from GIS-lab.info)
    @staticmethod
    def get_distance(llat1, llong1, llat2, llong2):
        rad = 6372795

        lat1 = llat1 * math.pi / 180.
        lat2 = llat2 * math.pi / 180.
        long1 = llong1 * math.pi / 180.
        long2 = llong2 * math.pi / 180.

        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cdelta
        ad = math.atan2(y, x)
        dist = ad * rad

        x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
        y = sdelta * cl2
        z = math.degrees(math.atan(-y / x))

        if x < 0:
            z += 180.

        z2 = (z + 180.) % 360. - 180.
        z2 = - math.radians(z2)
        anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
        angledeg = (anglerad2 * 180.) / math.pi

        return dist / 1000, angledeg
