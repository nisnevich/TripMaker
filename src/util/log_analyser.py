import json
import os

from src.const.constants import PATH_LOG, PATH_RESULTS
from src.entity.flightroute import FlightsRoute

SENTENCE_COUNT = "[COMPLETED] Count: "
SENTENCE_CC = ", c/c: "
CHAR_ROUTE_OPEN = "["
CHAR_ROUTE_CLOSE = "]"


class LogAnalyseUtil:
    @staticmethod
    def get_routes(*file_names, min_countries_count=None, path_log=PATH_RESULTS, max_cc=None):
        list_route = []
        for file_name in file_names:
            lines = open(os.path.join(path_log, file_name), 'r').read().splitlines()
            for counter in range(0, len(lines)):
                line = lines[counter]
                if SENTENCE_COUNT in line:
                    count_index = line.find(SENTENCE_COUNT) + len(SENTENCE_COUNT)
                    cc_index = line.find(SENTENCE_CC) + len(SENTENCE_CC)
                    count = int(''.join([(sym if sym.isdigit() else "") for sym in line[count_index:count_index + 5]]))
                    cc = int(''.join([(sym if sym.isdigit() else "") for sym in line[cc_index:cc_index + 5]]))
                    if max_cc is not None:
                        if cc > max_cc:
                            continue
                    if min_countries_count is not None:
                        if count < min_countries_count:
                            continue
                    route_str = ""
                    counter_local = counter + 3
                    while counter_local < len(lines):
                        if CHAR_ROUTE_CLOSE in lines[counter_local]:
                            break
                        route_str += lines[counter_local]
                        counter_local += 1
                    route_str = "[{}]".format(route_str)
                    list_route.append(FlightsRoute.from_json(json.loads(route_str)))
        return list_route
