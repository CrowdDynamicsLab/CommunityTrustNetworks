''' code for network formation model'''

import networkx as nx
import numpy as np
from random import choices

def new(N, alpha, Tau_a, Tau_b):
    ''' new graph with N many nodes '''

    G = nx.Graph()

    for node in range(N):
        tau = np.random.beta(Tau_a, Tau_b)
        type = choices(['orange','blue'], [alpha, 1-alpha])

        G.add_node(node+1, trust = tau, type = type)

    return G

def node_enters(G, alpha, Tau_a, Tau_b):
    ''' add a new node and return that node number '''

    tau = np.random.beta(Tau_a, Tau_b)
    type = choices(['orange','blue'], [alpha, 1-alpha])
    new_node_num = len(G.nodes())+1
    G.add_node(new_node_num, trust = tau, type = type)

    return new_node_num

def barabasi_albert_init(G):
    ''' BA edge formation for all nodes '''

    return None

def barabasi_albert_new(G):
    ''' one iteration of BA edge formation for new node '''

    return None

def form_edge(G, new_node, recs):
    ''' form one edge for the new node '''

    trust = G.nodes[new_node]['trust']
    trust_flag = choices(['y','n'], [trust, 1-trust])

    if trust_flag:
        if recs[new_node] is not None:
            G.add_edge(node, recs[new_node])
    else:
        barabasi_albert_new(G)
