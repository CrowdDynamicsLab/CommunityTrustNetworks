''' code to run simulation '''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import formation, recommendations, metrics, plotting

N = 50                          # number of nodes init
ntwk_iters = 10                 # network iters, how many nodes to add
total_nodes = N+ntwk_iters
extra_iters = 100               # extra iterations after all nodes have been added
sim_iters = 1                  # total number of times to run each iter
alpha = .5                      # node types

rho_list = [0, 10, 20, 30, 40, 50]
#rho_list = [30, 40]
#rho_list = [0]
#rho_list = [5,10,15]
Tau_list = [(2,20),(2,10),(2,5),(2,2),(5,2),(10,2),(20,2)]
#Tau_list = [(2,10),(2,2),(10,2)]
#Tau_list = [(5,2),(10,2),(20,2)]

results_arr1 = np.empty((len(rho_list), len(Tau_list), sim_iters))
results_arr2 = np.empty((len(rho_list), len(Tau_list), sim_iters))
#results_arr3 = np.empty((len(rho_list), len(Tau_list), sim_iters))
#results_arr4 = np.empty((len(rho_list), len(Tau_list), sim_iters))


# rho is public entity resource constraint
for idx_r, rho in enumerate(rho_list):
    # tau_a and tau_b give the dist for trust
    for idx_t, (Tau_a, Tau_b) in enumerate(Tau_list):
        for sim_it in range(sim_iters):
            print(rho, Tau_a, Tau_b, sim_it)
            num_accepted_prop = 0
            num_total_prop = 0
            num_recs_none = 0
            total_money_spent = 0
            # run many iterations of the network formation model
            for i in range(ntwk_iters+extra_iters):
                # if it's the first iteration then create the graph
                if i == 0:
                    G = formation.new(N, alpha, Tau_a, Tau_b)
                elif i <= ntwk_iters:
                    formation.node_enters(G, alpha, Tau_a, Tau_b, i)

                # public entity chooses rho-many agents
                chosen_agents = recommendations.agent_selection(G, rho, i)

                # public entity makes recommendations to the agents chosen
                recs, num_recs_not_found = recommendations.recommend(G, chosen_agents, fairness_func = metrics.triangles)
                num_recs_none += num_recs_not_found
                num_total_prop += len([x for x in recs.values() if x is not None])

                # one iteration of the network formation model with no new agents
                num_accept, amount_spent = formation.christakis(G, recs, i, transparent_agent_trust = True, payment_prop = 1)
                num_accepted_prop += num_accept
                total_money_spent += amount_spent

            tri = metrics.triangles(G)

            #trust_list = [node[1]['trust'] for node in G.nodes.data()]
            results_arr1[idx_r][idx_t][sim_it] = tri
            results_arr2[idx_r][idx_t][sim_it] = amount_spent
            #results_arr3[idx_r][idx_t][sim_it] = num_recs_none
            #results_arr4[idx_r][idx_t][sim_it] = tri
            #print(num_accepted_prop)

#print(results_arr)

new_rho_list = [x/G.number_of_nodes() for x in rho_list]

plotting.heat_map(results_arr1, new_rho_list, Tau_list, type = 'triangles', title = 'rho_vs_tau_triangles_spend1', save = True)
plotting.heat_map(results_arr2, new_rho_list, Tau_list, type = 'num_prop', title = 'rho_vs_tau_amount_spent1', save = True)
#plotting.heat_map(results_arr3, new_rho_list, Tau_list, type = 'num_prop', title = 'rho_vs_tau_num_none_recs', save = True)
#plotting.heat_map(results_arr4, new_rho_list, Tau_list, type = 'triangles', title = 'rho_vs_tau_triangles', save = True)

#plotting.vis_G(G)
