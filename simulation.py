''' code to run simulation '''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import formation, recommendations, metrics, plotting

N = 20                          # number of nodes init
ntwk_iters = 10                 # network iters, how many nodes to add
total_nodes = N+ntwk_iters
extra_iters = 100               # extra iterations after all nodes have been added
sim_iters = 2                   # total number of times to run each iter
alpha = .5                      # node types

results_dict = {}

# rho is public entity resource constraint
for rho in [5, 10]:
    #, 15, 20]:

    # tau_a and tau_b give the dist for trust
    for Tau_a, Tau_b in [(20,2), (15,2)]:
        #, (10,2), (5,2)]:
        apl_list = []
        for sim_it in range(sim_iters):
            # run many iterations of the network formation model
            for i in range(ntwk_iters+extra_iters):
                # if it's the first
                if i == 0:
                    G = formation.new(N, alpha, Tau_a, Tau_b)
                elif i <= ntwk_iters:
                    formation.node_enters(G, alpha, Tau_a, Tau_b, i)

                # public entity chooses rho-many agents
                chosen_agents = recommendations.agent_selection(G, rho, i)

                # public entity makes recommendations to the agents chosen
                recs = recommendations.recommend(G, chosen_agents, fairness_func = metrics.apl)

                # one iteration of the network formation model with no new
                formation.christakis(G, recs, i)

            apl_list.append(1/metrics.apl(G))

        # TODO: make this less stupid
        results_dict[(rho, Tau_a, Tau_b)] = apl_list

print(results_dict)

#plotting.vis_G(G)
