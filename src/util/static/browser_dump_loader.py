import json
import webbrowser
from datetime import datetime

from src.const.constants import PATH_ROUTE_DUMP, DATE_FORMAT
from src.entity.flightroute import FlightsRoute

# ------ Constants

IS_RANGE_ACTIVATED = True
RANGE_VALUE = 7

# ------ Code

URL_SEARCH_AS = "https://search.aviasales.ru/{orig}{date}{dest}1"
if IS_RANGE_ACTIVATED:
    URL_SEARCH_AS += "?delta=0&range={range_value}".format(range_value=RANGE_VALUE)

dump = open(PATH_ROUTE_DUMP, 'r').read()
route_flights = FlightsRoute.from_json(json.loads(dump))

visited_countries = set()
total_cost = 0
for f in route_flights:
    webbrowser.open(URL_SEARCH_AS.format(orig=f.orig_city, dest=f.dest_city,
                                         date=datetime.strftime(f.depart_date, "%d%m")))
