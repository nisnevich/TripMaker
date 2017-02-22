from src.model.requesting.requester.asl.requester_price_map import ASPricesMapRequester

FLIGHT_PROVIDER_AS = "AS"
FLIGHT_PROVIDER_SS = "SS"


class RequesterService:
    @staticmethod
    def get_flights_map(city_orig, config_requester, origin_date=None):
        prices_map = []
        for provider in config_requester.flights_providers:
            date_from, date_to = config_requester.get_date_period(origin_date)
            if provider == FLIGHT_PROVIDER_AS:
                prices_map.extend(ASPricesMapRequester.get_flights_map(city_orig, date_from, date_to))
            if provider == FLIGHT_PROVIDER_SS:
                raise NotImplementedError()
        return prices_map
