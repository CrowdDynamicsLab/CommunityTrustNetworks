''' code for network formation model'''

import networkx as nx
import numpy as np
from random import choice, choices, shuffle
from itertools import combinations


def new(N, alpha, Tau_a, Tau_b):
    ''' new graph with N many nodes '''

    G = nx.Graph()

    for node in range(N):
        tau = np.random.beta(Tau_a, Tau_b)
        type = choices(['orange','blue'], [alpha, 1-alpha])

        G.add_node(node+1, trust = tau, type = type[0], new = False, ref = False)

    return G

def node_enters(G, alpha, Tau_a, Tau_b):
    ''' add a new node and mark it as new '''

    tau = np.random.beta(Tau_a, Tau_b)
    type = choices(['orange','blue'], [alpha, 1-alpha])
    new_node_num = len(G.nodes())+1
    G.add_node(new_node_num, trust = tau, type = type[0], new = True, ref = True)

def christakis(G, recs):
    ''' run the christakis network formation model '''

    # each node gets a pairing
    node_list = list(G.nodes())
    shuffle(node_list)
    for node in node_list:
        trust = G.nodes[node]['trust']
        trust_flag = choices([1,0], [trust, 1-trust])[0]

        # TODO: what happens if the edge already exists for the choice

        # if the node chooses to trust the public entity, just add that edge
        if trust_flag:
            if recs[node] is not None:
                G.add_edge(node, recs[node])
        # if not, then do christakis network formation model
        else:
            # do pairing
            node_pair = get_pairing(G, node)

            # if this pairing works for both, then add edge
            if edge_util(G, node, node_pair) > 0 and edge_util(G, node_pair, node) > 0:
                G.add_edge(node, node_pair)

    return G

def get_pairing(G, node):
    ''' gets random (or not so random) pairing for christakis model '''
    if G.nodes[node]['new']:
        node_pair = choice([x for x in list(G.nodes()) if x != node])

    else:
        choice_set = [x for x in list(G.nodes()) if nx.has_path(G, x, node) and nx.shortest_path_length(G, x, node) == 2]
        if len(choice_set) == 0:
            node_pair = choice([x for x in list(G.nodes()) if x != node])
        else:
            node_pair = choice(choice_set)

    return node_pair

def edge_util(G, u, v):
    ''' returns utility to u from forming an edge with v '''

    b1 = -1
    b2 = 0
    omega = .25
    a1 = -.25
    a2 = 0
    a3 = 2.75
    a4 = 1.25
    eps = np.random.logistic()

    x_u = 1 if G.nodes[u]['type'] == 'orange' else 0
    x_v = 1 if G.nodes[v]['type'] == 'orange' else 0
    deg_v = G.degree(v)
    if nx.has_path(G, u, v):
        uv_2 = 1 if nx.shortest_path_length(G, u, v) == 2 else 0
        uv_3 = 1 if nx.shortest_path_length(G, u, v) == 3 else 0
    else:
        uv_2 = 0
        uv_3 = 0

    util = b1 + b2*x_v - (omega*(x_u-x_v)**2) + a1*deg_v + (a2*(deg_v)**2) + a3*uv_2 + a4*uv_3 + eps
    return util

def reset_nodes(G):
    ''' resets all nodes to not be new '''

    for node in G.nodes():
        G.nodes[node]['new'] = False
