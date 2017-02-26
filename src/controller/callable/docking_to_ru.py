# ----- System imports
import json

# ----- Local imports
import random
from queue import PriorityQueue

import networkx as nx

from src.const.constants import *
from src.entity.flightroute import FlightsRoute
from src.model.composing.filter.impl.country_target import TargetCountryFlightFilter
from src.model.composing.filter.impl.country_visited_exclude_cheap import VisitedCountryExcludeCheapFlightFilter
from src.model.composing.filter.impl.price_total import TotalPriceFlightFilter
from src.model.composing.ucs import UCSComposer
from src.model.requesting.configuration.configuration_requester import RequesterConfiguration
from src.util.graphutil import GraphUtil
from src.util.log import Logger


class FinishDockingCallableController:
    id_instance = random.getrandbits(128)

    def dock(self, route):
        Logger.info("Starting FinishDockingCallableController.dock() #{}".format(self.id_instance))

        filter_total_price = TotalPriceFlightFilter()
        filter_total_price.max_total_price = 20000 - route.get_price_total()
        filter_target = TargetCountryFlightFilter("RU")
        filter_target.allowable_price_error = 1000
        list_filters = [filter_target,
                        # VisitedCountryExcludeCheapFlightFilter(),
                        filter_total_price]

        graph_total = nx.MultiDiGraph()
        configuration_requester = RequesterConfiguration(route[-1].depart_date)

        Logger.error("Scanning flights from {}, visited countries: {}".format(route[-1].orig_city,
                                                                              route.get_countries_visited()))

        ucs_composer = UCSComposer()
        ucs_composer.queue = PriorityQueue()
        hash_code = random.getrandbits(128)
        ucs_composer.queue.put((0, hash_code))
        ucs_composer.map_routes_queue[hash_code] = (route[-1].orig_city, route)

        graph = ucs_composer.find_flights(route[-1].orig_city, configuration_requester, list_filters)

        Logger.info("Finished FinishDockingCallableController.dock() #{}".format(self.id_instance))

