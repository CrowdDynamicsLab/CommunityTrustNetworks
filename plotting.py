''' code for plotting networks and figs '''

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

def make_edge(x, y):
    return  go.Scatter(x         = x,
                       y         = y,
                       mode = 'lines',
                       line = dict(width = 10, color = 'gray'),
                       opacity = .5)

def graph_vis(G, colors):
    N = len(G.nodes())
    pos = nx.spring_layout(G, k = 1.2)
    edge_trace = []
    for edge in G.edges(data = True):
        char_1 = edge[0]
        char_2 = edge[1]
        x0, y0 = pos[char_1]
        x1, y1 = pos[char_2]
        trace  = make_edge([x0, x1, None], [y0, y1, None])
        edge_trace.append(trace)

    node_trace = go.Scatter(x         = [],
                            y         = [],
                            textposition = "top center",
                            textfont_size = 10,
                            hoverinfo = 'text',
                            hovertext = [],
                            text      = [],
                            mode      = 'markers+text',
                            marker    = dict(color = colors,
                                             size  = 50,
                                             symbol = 'circle',
                                             line=dict(color='white', width = 2)))
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    layout = go.Layout(xaxis = {'showgrid': False, 'zeroline': False},
                        yaxis = {'showgrid': False, 'zeroline': False},
                        autosize = False,
                        width = 1000,
                        height = 1000,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )

    # Create figure
    fig = go.Figure(layout = layout)
    for trace in edge_trace:
        fig.add_trace(trace)
    fig.add_trace(node_trace)
    fig.update_layout(showlegend = False)
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)
    fig.show()

def vis_G(G):

    N = len(list(G.nodes()))

    types = []
    color = []

    for node in G.nodes():
        types += tuple(([G.nodes()[node]['type']]))

    for i in range(len(types)):
        if types[i] == 'orange':
            color.append('rgb(245, 182, 66)')
        elif types[i] == 'blue':
            color.append('rgb(66, 153, 245)')

    graph_vis(G, color)

def heat_map(arr, dim1, dim2, type):
    return None
