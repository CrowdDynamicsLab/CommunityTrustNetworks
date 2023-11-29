''' code for network formation model'''

import networkx as nx
import numpy as np
from random import choices
from itertools import combinations

def new(N, alpha, hom, Tau_a, Tau_b):
    ''' new graph with N many nodes '''

    G = nx.Graph()

    for node in range(N):
        tau = np.random.beta(Tau_a, Tau_b)
        type = choices(['orange','blue'], [alpha, 1-alpha])
        attr = choices(['hom','het'], [hom, 1-hom])

        G.add_node(node+1, trust = tau, type = type[0], attr = attr[0])

    return G

def node_enters(G, alpha, hom, Tau_a, Tau_b):
    ''' add a new node and return that node number '''

    tau = np.random.beta(Tau_a, Tau_b)
    type = choices(['orange','blue'], [alpha, 1-alpha])
    attr = choices(['hom','het'], [hom, 1-hom])
    new_node_num = len(G.nodes())+1
    G.add_node(new_node_num, trust = tau, type = type[0], attr = attr[0])

    return new_node_num

# start with a clique that is a stable triad (from our paper)
def clique_init(G):
    ''' intial edges formed '''
    for node1, node2 in combinations(G.nodes(data = True), 2):
        if node1[1]['attr'] == 'hom' and node2[1]['attr'] == 'hom' and node1[1]['type'] == node2[1]['type']:
            G.add_edge(node1[0],node2[0])
        elif node1[1]['attr'] == 'het' and node2[1]['attr'] == 'het' and node1[1]['type'] != node2[1]['type']:
            G.add_edge(node1[0],node2[0])

def barabasi_albert_new(G):
    ''' one iteration of BA edge formation for new node '''

    return None

def form_edge(G, new_node, recs):
    ''' form one edge for the new node '''

    trust = G.nodes[new_node]['trust']
    trust_flag = choices([1,0], [trust, 1-trust])[0]
    if trust_flag:
        if recs[new_node] is not None:
            G.add_edge(new_node, recs[new_node])
    else:
        barabasi_albert_new(G)
