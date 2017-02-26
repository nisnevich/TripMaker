# ----- System imports

# ----- Local imports
import random
from datetime import datetime, timedelta

import networkx as nx

from src.const.constants import DATE_FORMAT
from src.model.composing.filter.impl.country_visited_exclude_cheap import VisitedCountryExcludeCheapFlightFilter
from src.model.composing.filter.impl.price_total import TotalPriceFlightFilter
from src.model.composing.filter.impl.route_docking import DockingRouteFlightFilter
from src.model.composing.ucs import UCSComposer
from src.model.requesting.configuration.configuration_requester import RequesterConfiguration
from src.util.graphutil import GraphUtil
from src.util.log import Logger
from src.util.log_analyser import LogAnalyseUtil


class StartDockingCallableController:

    id_instance = random.getrandbits(128)
    LOGS_MAX_CC = 1150
    LOGS_MIN_COUNTRIES_COUNT = 15

    # cheap_tip = ["BTS", "MUC", "MIL", "SKG", "NTE", "TLS", "MSQ"]
    list_cities_origin = ["MOW", "LED", "KGD", "PKV", "BZK", "EGO", "PES", "VOZ"]
    # list_cities_origin = ["MOW"]

    def dock(self, route):
        Logger.info("Starting StartDockingCallableController.dock() #{}".format(self.id_instance))

        # graph_total = nx.MultiDiGraph()
        counter = 1
        for city_origin in self.list_cities_origin:
            Logger.error("#{}) Selected airport: {}".format(counter, city_origin))
            counter += 1

            filter_total_price = TotalPriceFlightFilter()
            filter_total_price.max_total_price = 20000 - route.get_price_total()
            filter_docking = DockingRouteFlightFilter([route])
            filter_docking.allowable_price_error = 1000
            list_filters = [filter_docking,
                # VisitedCountryExcludeCheapFlightFilter(),
                filter_total_price]

            date_from = route[-1].depart_date - timedelta(days=30)

            configuration_requester = RequesterConfiguration(date_from)
            graph = UCSComposer().find_flights(city_origin, configuration_requester, list_filters)
            # GraphUtil.remove_duplicate_edges(graph)
            # GraphUtil.merge_graphs(graph_total, graph)

        # GraphUtil.draw_hierarhical(graph_total, "ru_total_{}-{}".format(graph_total.number_of_nodes(),
        #                                                                 graph_total.number_of_edges()), 0)

        Logger.info("Finished StartDockingCallableController.dock() #{}".format(self.id_instance))
