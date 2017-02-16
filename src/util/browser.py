import json
import webbrowser
from datetime import datetime

from src.const.constants import PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flightroute import FlightsRoute


class BrowserUtil:
    URL_SEARCH_AS = "https://search.aviasales.ru/{orig}{date}{dest}1"

    @staticmethod
    def scan_flights(*routes, range_value=0):
        for f in routes:
            webbrowser.open(BrowserUtil.create_link(f, range_value))

    @staticmethod
    def create_link(f, range_value=0):
        url = BrowserUtil.URL_SEARCH_AS

        if range_value > 0:
            url += "?delta=0&range={range_value}".format(range_value=range_value)

        return url.format(orig=f.orig_city, dest=f.dest_city,
                          date=datetime.strftime(f.depart_date, "%d%m"))
