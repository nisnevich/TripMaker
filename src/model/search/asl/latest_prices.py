# ----- System imports
from datetime import datetime
from time import sleep

# ----- Third-party imports
import requests

# ----- Local imports
from src.const.constants import ORIGIN_DATE_PERIOD, DATE_FORMAT, AS_ACCESS_TOKEN, MAX_CITY_DISTANCE, \
    TIMEOUT_SLEEP_CONNECTION_ERROR
from src.entity.flight import Flight
from src.util.distance import DistanceUtil
from src.util.logging import Logger
from src.util.progressbar import print_progress_bar


def get_lowest_prices_flights_list(orig_iata, date_from=None, date_to=None):
    request = ("http://map.aviasales.ru/supported_directions.json?origin_iata={orig_iata}&one_way=true"
               "&locale=en").format(orig_iata=orig_iata)
    try:
        list_directions_supported = requests.get(request).json()
    except ConnectionError as e:
        Logger.error(str(e))
        sleep(TIMEOUT_SLEEP_CONNECTION_ERROR)
        return get_lowest_prices_flights_list(orig_iata, date_from, date_to)

    if date_from is None:
        period = ORIGIN_DATE_PERIOD
    else:
        period = "month&beginning_of_period={date}".format(date=datetime.strftime(date_from.replace(day=1),
                                                                                  DATE_FORMAT))

    list_flights_cheapest = []
    for counter in range(0, len(list_directions_supported["directions"])):

        direction = list_directions_supported["directions"][counter]
        print_progress_bar(counter, len(list_directions_supported["directions"]),
                           prefix='Searching flights from {} for {}:'.format(orig_iata, period), suffix='Completed',
                           length=50)
        if orig_iata == direction["iata"]:
            # Yes, this is a real case ("Fly with AS API!")
            continue
        try:
            distance = DistanceUtil.get_city_distance(orig_iata, direction["iata"])
            if distance != -1:
                if MAX_CITY_DISTANCE < distance[0]:
                    continue
        except ValueError as e:
            Logger.debug("Strange thing happened. {}".format(e))
            continue

        request = ("http://api.travelpayouts.com/v2/prices/latest?origin={orig_iata}&destination={dest_iata}"
                   "&token={token}&one_way=true&sorting=price&currency=rub"
                   "&period_type={period}").format(orig_iata=orig_iata, dest_iata=direction["iata"],
                                                   period=period, token=AS_ACCESS_TOKEN)
        try:
            flights_supported = requests.get(request).json()["data"]
        except ConnectionError as e:
            Logger.error(str(e))
            sleep(TIMEOUT_SLEEP_CONNECTION_ERROR)
            counter -= 1
            continue

        if len(flights_supported) > 0:
            f = flights_supported[0]
            flight_cheapest = Flight(f['origin'], f['destination'],
                                     datetime.strptime(f['depart_date'], DATE_FORMAT), f['value'])
            list_flights_cheapest.append(flight_cheapest)

    if date_to is not None:
        if date_to.month - date_from.month != 0:
            list_flights_cheapest.extend(get_lowest_prices_flights_list(orig_iata, date_to))
        flights_filtered = []
        # Filter dates
        for f in list_flights_cheapest:
            if date_from <= f.depart_date <= date_to:
                flights_filtered.append(f)
        list_flights_cheapest = flights_filtered

    # Array may be empty
    if len(list_flights_cheapest) > 0:
        try:
            return sorted(list_flights_cheapest, key=lambda f: f.price, reverse=False)
        except TypeError as e:
            Logger.error("Strange thing happened. len(flights)={}, flights={}".format(len(list_flights_cheapest),
                                                                               list_flights_cheapest))
            Logger.error(str(e))
            return []
    else:
        return []
