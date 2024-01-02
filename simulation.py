''' code to run simulation '''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import formation, recommendations, metrics, plotting

N = 20                          # number of nodes init
ntwk_iters = 10                 # network iters, how many nodes to add
total_nodes = N+ntwk_iters
extra_iters = 100               # extra iterations after all nodes have been added
sim_iters = 5                   # total number of times to run each iter
alpha = .5                      # node types

rho_list = [5,10,15,20]
Tau_list = [(2,20),(2,10),(2,2),(10,2), (20,2)]

results_arr = np.empty((len(rho_list), len(Tau_list), sim_iters))

# rho is public entity resource constraint
for idx_r, rho in enumerate(rho_list):
    # tau_a and tau_b give the dist for trust
    for idx_t, (Tau_a, Tau_b) in enumerate(Tau_list):
        for sim_it in range(sim_iters):
            print(sim_it)
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
                recs = recommendations.recommend(G, chosen_agents, fairness_func = metrics.triangles)

                # one iteration of the network formation model with no new
                formation.christakis(G, recs, i)

            apl = metrics.apl(G)

            results_arr[idx_r][idx_t][sim_it] = apl

print(results_arr)

#plotting.heat_map(results_arr, rho_list, Tau_list, type = 'triangles', title = 'rho_vs_tau_test2', save = True)

#plotting.vis_G(G)
