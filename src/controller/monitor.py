# ----- System imports
import pprint

# ----- Local imports

from src.model.composing.monitor_russia_departures import RussiaDeparturesComposer
from src.util.log import Logger

pretty_printer = pprint.PrettyPrinter()
composer = RussiaDeparturesComposer()
date_period_list = ["2017-02-01:month", "2017-03-01:month", "2017-04-01:month"]
# date_period_list = ["2017-03-01:month", "2017-04-01:month", "2017-05-01:month", "2017-06-01:month", "2017-07-01:month"]

count_result, cost_result, countries_result, route_result = composer.start(["MOW"], date_period_list)

Logger.info("Best result: visited {} countries for {} rub: {}".format(count_result,
                                                                      cost_result, countries_result))
Logger.info("The route:")
Logger.info(route_result.to_json())
