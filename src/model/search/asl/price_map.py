# ----- System imports
from datetime import datetime

# ----- Third-party imports
import requests

# ----- Local imports
from src.const.constants import ORIGIN_DATE_PERIOD, DATE_FORMAT
from src.entity.flight import Flight
from src.model.search.asl.dto.flightadapter import ASFlightDTOAdapter
from src.util.log import Logger


def get_lowest_prices_flights_list(orig_iata, date_from=None, date_to=None, origin_period=ORIGIN_DATE_PERIOD):
    if date_from is None:
        period = origin_period
    else:
        period = datetime.strftime(date_from.replace(day=1), DATE_FORMAT) + ":month"

    request = ("http://map.aviasales.ru/prices.json?origin_iata={orig_iata}&period={period}"
               "&one_way=true").format(orig_iata=orig_iata, period=period)
    flights_data = requests.get(request).json()
    if "errors" in flights_data:
        Logger.debug("Response from API contains a error. error={}, orig_iata={}, date_from={}, "
                     "date_to={}, origin_period={}".format(flights_data["errors"], orig_iata, date_from,
                                                           date_to, origin_period))
        return []

    flights = [Flight(ASFlightDTOAdapter(f)) for f in flights_data]
    if date_to is not None:
        if date_to.month - date_from.month != 0:
            flights.extend(get_lowest_prices_flights_list(orig_iata, date_to))
        flights_filtered = []
        # Filter dates
        for f in flights:
            if date_from <= f.depart_date <= date_to:
                flights_filtered.append(f)
        flights = flights_filtered
    # Array may be empty
    if len(flights) > 0:
        try:
            return sorted(flights, key=lambda f: f.price, reverse=False)
        except TypeError as e:
            Logger.error("Strange thing happened. len(flights)={}, flights={}".format(len(flights), flights))
            Logger.error(str(e))
            return []
    else:
        return []
