''' code to run simulation '''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import formation, recommendations, metrics, plotting

ntwk_iters = 5                       # network iters, how many nodes to add
N = 20                          # number of nodes init
alpha = .5                      # node types
Tau_a = 20                      # trust dist, a param for beta dist
Tau_b = 2                       # trust dist, b param for beta dist
rho = 5                         # resource constraint of public entity

# run many iterations of the network formation model
for i in range(ntwk_iters):
    # if it's the first
    if i == 0:
        G = formation.new(N, alpha, Tau_a, Tau_b)
    else:
        formation.node_enters(G, alpha, Tau_a, Tau_b)

    # public entity chooses rho-many agents
    chosen_agents = recommendations.agent_selection(G, rho)

    # public entity makes recommendations to the agents chosen
    recs = recommendations.recommend(G, chosen_agents, fairness_func = metrics.apl)

    # one iteration of the network formation model with no new
    formation.christakis(G, recs)

    # resets all nodes to not be new
    formation.reset_nodes(G)
