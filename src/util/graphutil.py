import copy
import os

import pydotplus
from networkx.drawing.nx_pydot import write_dot
import plotly

plotly.tools.set_credentials_file(username='nisnevich', api_key='Uj2m8yNYSxPEzepWXdgu')
import plotly.plotly as py
from plotly.graph_objs import *

import networkx as nx
import matplotlib.pyplot as plt

from src.const.constants import PATH_LOG_GRAPHS


class GraphUtil:
    @staticmethod
    def remove_duplicate_edges(graph):
        for node_name in graph.nodes():
            directions = graph[node_name]
            for (direction_name, edges) in directions.items():
                map_dates = {}
                for i in edges:
                    flight = edges[i]["flight"]
                    if flight.depart_date not in map_dates:
                        map_dates[flight.depart_date] = copy.deepcopy(edges[i])
                    else:
                        if map_dates[flight.depart_date]["flight"].price > flight.price:
                            map_dates[flight.depart_date] = copy.deepcopy(edges[i])
                for i in range(0, len(edges)):
                    graph.remove_edge(node_name, direction_name)
                for edge in map_dates:
                    graph.add_edge(node_name, direction_name, flight=map_dates[edge]["flight"])

    @staticmethod
    def merge_graphs(g_to, g_from):
        g_to.add_nodes_from(g_from.nodes(data=True))

        for e in g_from.edges(data=True, keys=False):
            flight = e[2]["flight"]
            if not g_to.has_edge(e[0], e[1]):
                if e[0] not in g_to:
                    g_to.add_node(e[0], g_to.node[e[0]])
                if e[1] not in g_to:
                    g_to.add_node(e[1], g_to.node[e[1]])
                g_to.add_edge(e[0], e[1], attr_dict=e[2])
            else:
                list_edges = g_to.edge[e[0]][e[1]]
                if len(list_edges) == 1:
                    edge_flight = list_edges[0]["flight"]
                    if edge_flight.depart_date == flight.depart_date:
                        if edge_flight.price > flight.price:
                            g_to.edge[e[0]][e[1]][0]["flight"] = flight
                else:
                    min_price = 9999999
                    index_min_price = -1
                    for i in range(0, len(list_edges)):
                        edge = list_edges[i]
                        if edge["flight"].depart_date == flight.depart_date:
                            if edge["flight"].price < min_price:
                                min_price = edge["flight"].price
                                index_min_price = i
                    if min_price > flight.price:
                        g_to.edge[e[0]][e[1]][index_min_price]["flight"] = flight

    @staticmethod
    def draw(graph_draw, graph_name, figures_count):
        plt.figure(figures_count)
        build_plot(graph_draw)
        plt.axis('off')
        plt.savefig(os.path.join(PATH_LOG_GRAPHS, '{}.png'.format(graph_name)), bbox_inches='tight')

    @staticmethod
    def draw_hierarhical(graph_draw, graph_name, figures_count):
        path_dot = os.path.join(PATH_LOG_GRAPHS, 'dots/{}.dot'.format(graph_name))
        path_image = os.path.join(PATH_LOG_GRAPHS, 'images/{}.png'.format(graph_name))
        path_dump = os.path.join(PATH_LOG_GRAPHS, 'dumps_pickle/{}.pickle'.format(graph_name))
        write_dot(graph_draw, path_dot)
        pydotplus.graph_from_dot_file(path_dot).write_png(path_image)
        nx.write_gpickle(graph_draw, path_dump)

    @staticmethod
    def show(graph_draw, figures_count=0):
        plt.figure(figures_count)
        build_plot(graph_draw)
        plt.axis('off')
        plt.show()

    @staticmethod
    def show_beautiful_plotly(graph):
        # FIXME this peace doesn't work
        pos = nx.get_node_attributes(graph, 'pos')
        dmin = 1
        ncenter = 0
        for n in pos:
            x, y = pos[n]
            d = (x - 0.5) ** 2 + (y - 0.5) ** 2
            if d < dmin:
                ncenter = n
                dmin = d

        p = nx.single_source_shortest_path_length(graph, ncenter)

        edge_trace = Scatter(
            x=[],
            y=[],
            line=Line(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in graph.edges():
            x0, y0 = graph.node[edge[0]]['pos']
            x1, y1 = graph.node[edge[1]]['pos']
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]

        node_trace = Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=Marker(
                showscale=True,
                # colorscale options
                # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
                # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
                colorscale='YIGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

        for node in graph.nodes():
            x, y = graph.node[node]['pos']
            node_trace['x'].append(x)
            node_trace['y'].append(y)

        for node, adjacencies in enumerate(graph.adjacency_list()):
            node_trace['marker']['color'].append(len(adjacencies))
            node_info = '# of connections: ' + str(len(adjacencies))
            node_trace['text'].append(node_info)

        fig = Figure(data=Data([edge_trace, node_trace]),
                     layout=Layout(
                         title='<br>Network graph made with Python',
                         titlefont=dict(size=16),
                         showlegend=False,
                         width=650,
                         height=650,
                         hovermode='closest',
                         margin=dict(b=20, l=5, r=5, t=40),
                         annotations=[dict(
                             text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                             showarrow=False,
                             xref="paper", yref="paper",
                             x=0.005, y=-0.002)],
                         xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
        py.plot(fig, filename='networkx')


def build_plot(graph_draw):
    pos = nx.spring_layout(graph_draw)

    nx.draw_networkx_nodes(graph_draw, pos=pos, linewidths=0.1, alpha=0.8)
    nx.draw_networkx_edges(graph_draw, pos=pos, width=0.1, arrows=True)

    labels_nodes = {}
    for node in graph_draw.nodes():
        labels_nodes[node] = node
    nx.draw_networkx_labels(graph_draw, pos, labels_nodes, font_size=12, font_color='black')

    # labels_edges = {}
    # for edge in G.edges():
    #     labels_edges[edge] = edge
    # nx.draw_networkx_edge_labels(G, pos, labels=labels_edges, font_size=12, font_color='green')


def build_hierarhical_plot(graph_draw):
    pos = nx.spring_layout(graph_draw)

    nx.draw_networkx_nodes(graph_draw, pos=pos, linewidths=0.1, alpha=0.8)
    nx.draw_networkx_edges(graph_draw, pos=pos, width=0.1, arrows=True)

    labels_nodes = {}
    for node in graph_draw.nodes():
        labels_nodes[node] = node
    nx.draw_networkx_labels(graph_draw, pos, labels_nodes, font_size=12, font_color='black')

    # labels_edges = {}
    # for edge in G.edges():
    #     labels_edges[edge] = edge
    # nx.draw_networkx_edge_labels(G, pos, labels=labels_edges, font_size=12, font_color='green')
