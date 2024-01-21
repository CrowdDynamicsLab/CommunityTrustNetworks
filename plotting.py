''' code for plotting networks and figs '''

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

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

def heat_map(arr, dim1, dim2, type, title, save):

    avg_arr = np.mean(arr, axis = 2)

    data = np.rot90(avg_arr)

    x_tick_labels = np.round(dim1,2)
    y_tick_labels = dim2[::-1]
    ax = None

    if type == 'apl' :
        ax = sns.heatmap(data, vmin = 0, vmax = 1,
                 annot=True, cbar=True, square=True,
                 xticklabels = x_tick_labels, yticklabels = y_tick_labels, linewidth=0.5)

    if type == 'triangles':
        ax = sns.heatmap(data, vmin = 0, vmax = .075,
                 annot=True, cbar=True, square=True,
                 xticklabels = x_tick_labels, yticklabels = y_tick_labels, linewidth=0.5)

    if type == 'num_prop':
        ax = sns.heatmap(data, vmin = 0,
                 annot=True, cbar=True, square=True,
                 xticklabels = x_tick_labels, yticklabels = y_tick_labels, linewidth=0.5)

    if type == 'spent':
        ax = sns.heatmap(data, vmin = 0, vmax = 150,
                 annot=True, cbar=True, square=True,
                 xticklabels = x_tick_labels, yticklabels = y_tick_labels, linewidth=0.5, fmt='.2f')

    ax.set_xlabel('Resource Constraint')
    ax.set_ylabel('Agent Trust')
    ax.tick_params(axis='both', which='major', labelsize=10)

    cbar_axes = ax.figure.axes[-1]

    if save:
        title_save = 'figs/' + title +'.pdf'
        plt.savefig(title_save, dpi = 300, bbox_inches = 'tight')
        plt.close('all')
    else:
        plt.show()

def surface_plot(arr, dim1, dim2, type, title, save):

    avg_arr = np.mean(arr, axis = 2)

    data = np.rot90(avg_arr)


    n = len(dim1)
    m = len(dim2)

    tau = np.repeat(dim2, n)[::-1]

    rho = (np.tile(dim1, m))[::-1]

    data = np.fliplr(data)

    df = pd.DataFrame({"rho":rho.reshape(n*m,), "tau":tau.reshape(n*m,), "tri":data.reshape(n*m,)}, index=range(0,n*m))

    #print(df)

    #print(df.head(27))

    X, y = df[["rho", "tau"]], df["tri"]
    poly = PolynomialFeatures(degree=2, include_bias=False)
    poly_features = poly.fit_transform(X)
    poly_reg_model = LinearRegression()
    poly_reg_model.fit(poly_features, y)

    i = poly_reg_model.intercept_
    c = poly_reg_model.coef_

    print(i,c)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})


    tau = np.arange(0, 1.00, 1/100)
    rho = np.arange(0, 2, 1/100)

    R,T = np.meshgrid(rho, tau)
    tri = i + c[0]*R + c[1]*T + c[2]*(R**2) + c[3]*(T**2) + c[4]*T*R

    surf = ax.plot_surface(R, T, tri, cmap = sns.cm.rocket ,vmin =0, vmax = .1,
                           linewidth=0, antialiased=False)

    fig.colorbar(surf, shrink = .4)

    ax.view_init(25, 220)
    #ax.view_init(270, 0)

    ax.set_xlabel('Resource Constraint')
    ax.set_ylabel('Agent Trust')
    ax.tick_params(axis='both', which='major', labelsize=10)
    if save:
        title_save = 'figs/' + title +'.pdf'
        plt.savefig(title_save, dpi = 300, bbox_inches = 'tight')
        plt.close('all')
    else:
        plt.show()
