from abc import ABCMeta, abstractmethod
from time import sleep

import requests

from src.const.constants import TIMEOUT_SLEEP_CONNECTION_ERROR
from src.util.gmail_api import GmailAPIUtil
from src.util.log import Logger


body_error = '''
Hi, man.

Got a problem here. Connection error, man. The message: {error_message}

I was trying to connect again and again with the interval of {interval} seconds, and it took {spent_time} minutes to establish the connection.

So, don't worry, now connection is established.

TripMaker bot
'''

class AbstractPriceMapRequester:
    __metaclass__ = ABCMeta

    # FIXME make this field 'volatile'!
    connection_error_occurred = False

    @staticmethod
    @abstractmethod
    def get_flights_map(city_origin, date_from, date_to):
        pass

    @staticmethod
    def send_get(request):
        flights_data = None
        count_attempts = 0
        while flights_data is None:
            try:
                flights_data = requests.get(request).json()
            except Exception as e:
                Logger.error("Cannot send request: {}. Waiting for {} seconds..."
                             "".format(str(e), TIMEOUT_SLEEP_CONNECTION_ERROR))
                count_attempts += 1
                sleep(TIMEOUT_SLEEP_CONNECTION_ERROR)
        return flights_data
        # if count_attempts > 0:
        #     # send OK notification
        #     print()

    def send_email(self, error_message, interval, attempts):
        spent_time = round(interval * attempts / 60)
        subject = "[TripMaker] Connection error occurred (took {} mins to fix)".format(spent_time)
        body = body_error.format(error_message=error_message, interval=interval, spent_time=spent_time)
        message = GmailAPIUtil.create_message("me", "officialsagorbox@gmail.com", subject, body)

        GmailAPIUtil.send_message(GmailAPIUtil.create_service(), "me", message)
        Logger.error("Sending: {}".format(subject))
