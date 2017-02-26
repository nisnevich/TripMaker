import os

import networkx as nx
from networkx.drawing.nx_pydot import read_dot

import pydotplus

from src.const.constants import PATH_LOG_GRAPHS

graph_name = "2627_403_03_20-19"
path_dot = os.path.join(PATH_LOG_GRAPHS, 'dots/{}.dot'.format(graph_name))
# graph = pydotplus.graph_from_dot_file(path_dot)
graph = nx.read_gpickle(path_dot)
# graph = read_dot(path_dot)

print()
