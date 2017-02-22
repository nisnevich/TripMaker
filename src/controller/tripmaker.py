# ----- System imports
import pprint

# ----- Local imports
from datetime import datetime

from src.const.constants import *
from src.model.composing.dfs import DFSComposer
from src.model.composing.filter.impl.country_visited_exclude_cheap import VisitedCountryExcludeCheapFlightFilter
from src.model.composing.filter.impl.esoteric.price_stupid import StupidPriceFlightFilter
from src.model.composing.filter.impl.price import PriceFlightFilter
from src.model.composing.filter.impl.price_total import TotalPriceFlightFilter

from src.model.requesting.configuration.configuration_requester import RequesterConfiguration

pretty_printer = pprint.PrettyPrinter()
dfs_composer = DFSComposer()
configuration_requester = RequesterConfiguration(datetime(2017, 3, 1))

list_filters = [PriceFlightFilter(), StupidPriceFlightFilter(), VisitedCountryExcludeCheapFlightFilter(),
                TotalPriceFlightFilter()]

for orig_iata in DEFAULT_ORIGIN_IATA:
    graph = dfs_composer.find_flights(orig_iata, configuration_requester, list_filters)
