from src.util.lib.graphsearch import single_source_dijkstra


class DijkstraSearcher:
    def __init__(self):
        self.distances = {}
        self.paths = {}

    def get_cost_route(self, origin, target, graph=None, enable_cache_update=False):
        def get_weight(e, e_index):
            return e[e_index]["flight"].price
        if graph is not None:
            assert origin in graph
            if enable_cache_update or origin not in self.distances:
                distances, paths = single_source_dijkstra(graph, origin, get_weight=get_weight)
                self.distances[origin] = distances
                self.paths[origin] = paths
        if origin not in self.distances:
            return None
        if target not in self.paths[origin]:
            return -1
        return self.distances[origin][target], self.paths[origin][target]
        # length_max = 0
        # for city in self.cache[origin]:
        #     dates_departure = self.cache[origin][city]
        #     for date in dates_departure:
        #         if isinstance(date, datetime):
        #             if dates_departure[date] > length_max:
