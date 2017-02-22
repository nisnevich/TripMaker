import json
import os
import webbrowser
from datetime import datetime

from src.const.constants import PATH_LOG_MAPS, PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flightroute import FlightsRoute
from src.util import gmplot_mod
from src.util.browser import BrowserUtil
from src.util.country import CountryUtil
from src.util.distance import DistanceUtil
from src.util.log import Logger

MAX_COLOR_COMPONENT = 255


class FlightsMapDrawer:
    @staticmethod
    def rgb_to_hex(rgb):
        ''' [255,255,255] -> "#FFFFFF" '''
        rgb = [int(x) for x in rgb]
        return "#" + "".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in rgb])

    @staticmethod
    def get_proportion_color(max_price, min_price, current_price):
        blue_component = 0

        max_price_normalized = max_price - min_price
        current_price_normalized = current_price - min_price
        half_price = max_price_normalized / 2

        if max_price_normalized == 0:
            red_component = 0
            green_component = MAX_COLOR_COMPONENT
        elif current_price - min_price < half_price:
            # red is increasing, green is maximal
            red_component = current_price_normalized * MAX_COLOR_COMPONENT / half_price
            green_component = MAX_COLOR_COMPONENT
        else:
            # red is maximal, green is decreasing
            current_price_normalized -= half_price
            red_component = MAX_COLOR_COMPONENT
            green_component = MAX_COLOR_COMPONENT - current_price_normalized * MAX_COLOR_COMPONENT / half_price

        return FlightsMapDrawer.rgb_to_hex([red_component, green_component, blue_component])

    @staticmethod
    def draw(flights, browser_open=False, center_map=None):

        if center_map is None:
            center_map = dict(lat=54.0020096, lon=21.7779824, zoom=4)
        gmap = gmplot_mod.GoogleMapPlotter(center_map["lat"], center_map["lon"], center_map["zoom"])
        counter = 0

        min_price = 9999999
        max_price = 0
        for f in flights:
            if f.price > max_price:
                max_price = f.price
            if f.price < min_price:
                min_price = f.price

        distance_total = 0
        price_total = 0

        for f in flights:
            info_orig = CountryUtil.get_info(f.orig_city)
            info_dest = CountryUtil.get_info(f.dest_city)

            if (info_orig is None) | (info_dest is None):
                Logger.error("Cannot draw country: no information available. "
                             "{}={}, {}={}".format(f.orig_city, info_orig, f.dest_city, info_dest))
                return False

            coords_orig = info_orig["coordinates"]
            coords_dest = info_dest["coordinates"]
            if (coords_orig == "null") | (coords_dest == "null"):
                Logger.error("Cannot draw country: no coordinates available. "
                             "{}={}, {}={}".format(f.orig_city, coords_orig, f.dest_city, coords_dest))
                return False

            latitudes = [coords_orig["lat"], coords_dest["lat"]]
            longitudes = [coords_orig["lon"], coords_dest["lon"]]

            distance_total += DistanceUtil.get_city_distance(f.orig_city, f.dest_city)[0]
            price_total += f.price

            if counter == 0:
                gmap.marker(coords_orig["lat"], coords_orig["lon"],
                            color="blue", title="The origin: {} ({})".format(info_orig["name"],
                                                                             info_orig["country_code"]))
            if counter == len(flights) - 1:
                gmap.marker(coords_dest["lat"], coords_dest["lon"],
                            color="blue", title="The destination: {} ({})".format(info_dest["name"],
                                                                                  info_dest["country_code"]))

            edge_text = "<a href='{link}' target='blank'>{orig_city} ({orig_country}) - {dest_city} ({dest_country}) " \
                        "at {date} for {cost} rub<br></a>".format(orig_city=info_orig["name"],
                                                                  orig_country=info_orig["country_code"],
                                                                  dest_city=info_dest["name"],
                                                                  dest_country=info_dest["country_code"],
                                                                  date=datetime.strftime(f.depart_date, DATE_FORMAT),
                                                                  cost=f.price, link=BrowserUtil.create_link(f))
            color = FlightsMapDrawer.get_proportion_color(max_price, min_price, f.price)

            # for i in range(0, len(latitudes)):
            #     gmap.marker(latitudes[i], longitudes[i], color="blue", title="City{}".format(i))
            gmap.plot(latitudes, longitudes, color, edge_width=3, edge_text=edge_text, edge_alpha=0.7)
            counter += 1

        gmap.alert("Total distance: {} km; total price: {} rub;"
                   " price for km: {} rub".format(round(distance_total),
                                                  price_total,
                                                  round(price_total/distance_total, 1)))
        path = os.path.join(PATH_LOG_MAPS, "map.html")
        gmap.draw(path)
        if browser_open:
            webbrowser.open(path)
        return True

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

FlightsMapDrawer.draw(route_flights, browser_open=True)
