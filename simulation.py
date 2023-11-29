''' code to run simulation '''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import formation, recommendations, metrics, plotting

iters = 5                       # network iters, how many nodes to add
N = 5                           # number of nodes init
alpha = .5                      # node types
hom = .5                        # prob of homophily
Tau_a = 20                      # trust dist, a param for beta dist
Tau_b = 2                       # trust dist, b param for beta dist
rho = 5                         # resource constraint of public entity

G = formation.new(N, alpha, hom, Tau_a, Tau_b)
formation.clique_init(G)

# each iteration, a new node joins
for i in range(iters):
    # node enters
    new_node = formation.node_enters(G, alpha, hom, Tau_a, Tau_b)

    # public entity chooses rho-many agents
    chosen_agents = recommendations.agent_selection(G, rho)

    # public entity makes recommendations to the agents chosen
    recs = recommendations.recommend(G, chosen_agents)

    # nodes form edges based on these recommendations and also network formation model
    formation.form_edge(G, new_node, recs)

    #for node in G.nodes(data = True):
    #    print(node)
    #for edge in G.edges():
#        print(edge)
