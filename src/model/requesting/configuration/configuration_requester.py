from datetime import timedelta

from src.const.constants import MIN_DAYS_PER_COUNTRY, MAX_DAYS_PER_COUNTRY
from src.model.requesting.service_requester import FLIGHT_PROVIDER_AS


class RequesterConfiguration:
    flights_providers = [FLIGHT_PROVIDER_AS]

    def __init__(self, start_date, min_interval=MIN_DAYS_PER_COUNTRY, max_interval=MAX_DAYS_PER_COUNTRY,
                 count_days_first_period=30):
        self.start_date = start_date
        self.min_days_per_country = min_interval
        self.max_days_per_country = max_interval
        self.days_in_first_period = count_days_first_period

    def get_date_period(self, date_origin=None):
        if date_origin is None:
            date_from = self.start_date
            date_to = self.start_date + timedelta(days=self.days_in_first_period)
        else:
            date_from = date_origin + timedelta(days=self.min_days_per_country)
            date_to = date_origin + timedelta(days=self.max_days_per_country)
        return date_from, date_to
