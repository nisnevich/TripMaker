import time
import json
import pprint
from queue import PriorityQueue
from datetime import timedelta

from src.const.constants import MIN_DAYS_PER_COUNTRY, MAX_DAYS_PER_COUNTRY, MAX_BILL_PRICE_RU, MAX_BILL_PRICE_EU, \
    MAX_BILL_PRICE_GENERIC, MAX_BILL_PRICE_INSIDE_COUNTRY, MAX_TOTAL_PRICE, ORIGIN_DATE_PERIOD, DATE_FORMAT
from src.entity.flight import Flight
from src.entity.flightroute import FlightsRoute
from src.model.search.asl.price_map import get_lowest_prices_flights_list
from src.util.browser import BrowserUtil
from src.util.country import CountryUtil
from src.util.gmail_api import GmailAPIUtil
from src.util.log import Logger

body_better = '''Hello, dear

Good news. I found a better price than before - from {iata_city_orig} ({iata_country_orig}) to {iata_city_dest} ({iata_country_dest}) at {depart_date_new} for just {new_price} rub ({delta_price} rub cheaper than the previous).

Check it here, please: {search_link}

Details:
IATA cities:    {iata_city_orig} - {iata_city_dest}
IATA countries: {iata_country_orig} - {iata_country_dest}
Depart date:    {depart_date_new}
Actual price:    {new_price} rub
Previous price: {old_price} rub
Was found at:   {found_at}

TripMaker bot
'''

body_new = '''Hello, dear

I found a flight with a really good price - from {iata_city_orig} ({iata_country_orig}) to {iata_city_dest} ({iata_country_dest}) at {depart_date_new} for just {new_price} rub.

Check it here, please: {search_link}

Details:
IATA cities:    {iata_city_orig} - {iata_city_dest}
IATA countries: {iata_country_orig} - {iata_country_dest}
Depart date:    {depart_date_new}
Actual price:   {new_price} rub
Was found at:   {found_at}

TripMaker bot
'''


class RussiaDeparturesComposer:
    lowest_prices = {}
    countries_visited = {'RU', 'FR', 'BG', 'IT', 'ES', 'PT', 'CH', 'DE', 'RO', 'GB', 'BE'}

    def filter_flights(self, origin_iata, origin_period, date_from = None, date_to = None):

        flights_list = get_lowest_prices_flights_list(origin_iata, date_from, date_to, origin_period=origin_period)
        orig_country = CountryUtil.get_country(origin_iata)

        for flight in flights_list:
            try:
                flight.orig_country = orig_country
                flight.dest_country = CountryUtil.get_country(flight.dest_city)
            except ValueError as e:
                Logger.debug("[IGNORE:NOT_FOUND] " + str(e))
                continue

            if (flight.orig_country == "RU") & (flight.dest_country == "RU"):
                if (flight.price > MAX_BILL_PRICE_RU) | (flight.price < 1200):
                    Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                                  "too expensive for Russia!").format(flight.orig_city, flight.dest_city, flight.price))
                    break
            elif CountryUtil.is_airport_european(flight.orig_city):
                if flight.price > MAX_BILL_PRICE_EU:
                    Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                                  "too expensive for Europe!").format(flight.orig_city, flight.dest_city, flight.price))
                    break
            elif flight.price > MAX_BILL_PRICE_GENERIC:
                Logger.debug(("[IGNORE:HIGH_PRICE] Breaking trip on the flight from {} to {} (for {} rub): "
                              "too expensive!").format(flight.orig_city, flight.dest_city, flight.price))
                break

            if flight.dest_country in self.countries_visited:
                Logger.info(("[IGNORE:ALREADY_VISITED] Ignore flight from {} to {} (for {} rub): "
                              "{} already visited!").format(flight.orig_city, flight.dest_city, flight.price,
                                                            flight.dest_country))
                continue

            if flight.price < MAX_BILL_PRICE_RU:
                Logger.info(
                    "Flying from {} ({}) to {} ({}) for {} rub at {}!".format(flight.orig_city, flight.orig_country,
                                                                              flight.dest_city, flight.dest_country,
                                                                              flight.price, flight.depart_date))
                entry = (flight.orig_city, flight.dest_city)
                if entry in self.lowest_prices:
                    if flight.price < self.lowest_prices[entry]:
                        old_price = self.lowest_prices[entry]
                        self.lowest_prices[entry] = flight.price
                        link = BrowserUtil.create_link(flight)
                        subject = "[TripMaker] Found better price for {}-{} ({})".format(flight.orig_city,
                                                                                         flight.dest_city, flight.price)
                        body = body_better.format(iata_city_orig=flight.orig_city, iata_city_dest=flight.dest_city,
                                                  iata_country_orig=flight.orig_country,
                                                  iata_country_dest=flight.dest_country,
                                                  depart_date_new=flight.depart_date, found_at=flight.found_at,
                                                  search_link=link, new_price=flight.price, old_price=old_price,
                                                  delta_price=(old_price - flight.price))
                        message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)

                        GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
                        Logger.info("Sending: {}, link : {}".format(flight.to_json(DATE_FORMAT), link))

                else:
                    self.lowest_prices[entry] = flight.price
                    link = BrowserUtil.create_link(flight)
                    subject = "[TripMaker] Found good price for {}-{} ({})".format(flight.orig_city,
                                                                                   flight.dest_city, flight.price)
                    body = body_new.format(iata_city_orig=flight.orig_city, iata_city_dest=flight.dest_city,
                                           iata_country_orig=flight.orig_country, iata_country_dest=flight.dest_country,
                                           depart_date_new=flight.depart_date, found_at=flight.found_at,
                                           search_link=link, new_price=flight.price)
                    message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)
                    GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
                    Logger.info("Sending: {}, link : {}".format(flight.to_json(DATE_FORMAT), link))
            else:
                break

    def start(self, orig_iata_list, date_period_list, date_from = None, date_to = None):

        date_counter = 0
        while True:
            origin_period = date_period_list[date_counter % len(date_period_list)]
            Logger.debug("Switched date to {}".format(origin_period))
            for orig_iata in orig_iata_list:
                Logger.debug("Scanning " + orig_iata)
                self.filter_flights(orig_iata, origin_period, date_from, date_to)
                time.sleep(5)
            date_counter += 1
