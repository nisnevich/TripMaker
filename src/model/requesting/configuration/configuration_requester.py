from datetime import timedelta

from src.model.requesting.service_requester import FLIGHT_PROVIDER_AS


class RequesterConfiguration:
    MAX_DAYS_START = 30

    flights_providers = [FLIGHT_PROVIDER_AS]

    min_days_per_country = 1
    max_days_per_country = 7
    start_date = None

    def __init__(self, start_date, min_interval=min_days_per_country, max_interval=max_days_per_country):
        self.start_date = start_date
        self.min_days_per_country = min_interval
        self.max_days_per_country = max_interval

    def get_date_period(self, date_origin=None):
        if date_origin is None:
            date_from = self.start_date
            date_to = self.start_date + timedelta(days=self.MAX_DAYS_START)
        else:
            date_from = date_origin + timedelta(days=self.min_days_per_country)
            date_to = date_origin + timedelta(days=self.max_days_per_country)
        return date_from, date_to
