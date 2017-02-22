# ----- System imports
from datetime import datetime

# ----- Third-party imports
import requests
from dateutil.relativedelta import *

# ----- Local imports
from src.const.constants import DATE_FORMAT
from src.entity.flight import Flight
from src.model.requesting.dto.flightadapter import ASFlightDTOAdapter
from src.model.requesting.requester.requester_abstract import AbstractPriceMapRequester
from src.util.date import DateUtil
from src.util.log import Logger


class ASPricesMapRequester(AbstractPriceMapRequester):
    DATE_FORMAT = "%Y-%m-%d"

    @staticmethod
    def get_flights_map(city_origin, date_from, date_to):
        flights = []
        count_period_months = 1 + DateUtil.diff_month(date_to, date_from)

        for delta_month in range(0, count_period_months):
            period_month = date_from.replace(day=1) + relativedelta(months=delta_month)
            period = datetime.strftime(period_month, DATE_FORMAT) + ":month"

            request = ("http://map.aviasales.ru/prices.json?origin_iata={city_origin}&period={period}"
                       "&one_way=true").format(city_origin=city_origin, period=period)
            flights_data = requests.get(request).json()
            if "errors" in flights_data:
                Logger.debug("Response from API contains a error. error={}, orig_iata={}, date_from={}, "
                             "date_to={}, period={}".format(flights_data["errors"], city_origin, date_from,
                                                            date_to, period))
                return []

            flights.extend([Flight(ASFlightDTOAdapter(f)) for f in flights_data])
        flights_filtered = []
        for f in flights:
            if date_from <= f.depart_date <= date_to:
                flights_filtered.append(f)
        # Array may be empty
        if len(flights_filtered) > 0:
            try:
                return sorted(flights_filtered, key=lambda f: f.price, reverse=False)
            except TypeError as e:
                Logger.error("Strange thing happened. len(flights)={}, flights={}".format(len(flights), flights))
                Logger.error(str(e))
                return []
        else:
            return []
