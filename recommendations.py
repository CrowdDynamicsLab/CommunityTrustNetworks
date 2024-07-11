''' code for public entity to make recommendations'''

import random
import metrics
import networkx as nx
import numpy as np

def agent_selection(G, rho, it, ad_campaign = False, ad_tradeoff = 0):
    ''' choose rho many agents to give recs to '''

    money_spent = 0

    if ad_campaign:
        ad_rho = int(np.floor(rho*ad_tradeoff))
        rho = rho - ad_rho
        money_spent = entity_ad_campaign(G, ad_rho)

    ranked_agents = []

    # rank the new and old agents separately
    new_agents = [x for x in list(G.nodes()) if G.nodes[x]['arrived'] != 0]
    new_agents = sorted(new_agents, key=lambda n: G.nodes[n]['arrived'], reverse = True)

    old_agents = [y for y in list(G.nodes()) if G.nodes[y]['arrived'] == 0]

    ranked_agents = new_agents

    # scramble the old agents and extend the ranking list
    random.shuffle(old_agents)
    ranked_agents.extend(old_agents)

    # make sure everything is ranked
    assert len(ranked_agents) == G.number_of_nodes()

    return ranked_agents[:rho], money_spent

def recommend(G, nodes, fairness_func):
    ''' return the recs for the chosen agents as a dict '''

    num_edges = G.number_of_edges()

    num_recs_not_found = 0

    recs = {key: None for key in list(G.nodes())}
    for node in nodes:
        best_choice = None
        best_fairness = 0
        choices = [x for x in list(G.nodes()) if x != node and x not in G.neighbors(node)]
        for choice in choices:

            # make sure didn't mess up edge addition and deletion
            assert G.number_of_edges() == num_edges

            G.add_edge(node, choice)
            fairness = fairness_func(G)
            G.remove_edge(node, choice)

            if fairness > best_fairness:
                best_fairness = fairness
                best_choice = choice

        if best_choice is None:
            num_recs_not_found += 1

        recs[node] = best_choice
    return recs, num_recs_not_found

def entity_announcement(G_old, G, transparent_entity = False, announcement_method = None):
    ''' entity announces what improvement it made to the network last iteration'''

    if transparent_entity:
        # entity tells the whole network the same thing
        if announcement_method == 'global':
            old_fairness = metrics.triangles(G_old)
            new_fairness = metrics.triangles(G)

            improvement = new_fairness-old_fairness

            for node in G.nodes():
                G.nodes[node]['trust'] = min([G.nodes[node]['trust'] + .71*improvement,1])

        # entity gives each node a specific announcement
        elif announcement_method == 'local':

            for node in G_old.nodes():
                new_fairness = 0
                old_fairness = 0

                neighbor_list_old = list(G_old.neighbors(node))
                neighbor_list_old.append(node)

                neighbor_list_new = list(G.neighbors(node))
                neighbor_list_new.append(node)

                node_subgraph_old = nx.induced_subgraph(G_old, neighbor_list_old)
                node_subgraph_new = nx.induced_subgraph(G, neighbor_list_new)

                if node_subgraph_old.number_of_nodes() >= 3:
                    old_fairness = metrics.triangles(node_subgraph_old)

                if node_subgraph_new.number_of_nodes() >= 3:
                    new_fairness = metrics.triangles(node_subgraph_new)

                improvement = new_fairness-old_fairness

                G.nodes[node]['trust'] = min([G.nodes[node]['trust'] + .48*improvement,1])

def entity_ad_campaign(G, ad_rho):
    ''' entity decides to advertise to a set of ad_rho-many agents to increase their trust'''

    trust_restoration = .71
    money_spent = 0

    agents = [x for x in list(G.nodes())]

    agents = sorted(agents, key=lambda m: G.nodes[m]['trust'])

    for node in agents[:ad_rho]:
        money = (1 - G.nodes[node]['trust'])
        G.nodes[node]['trust'] = min([G.nodes[node]['trust'] + trust_restoration*money,1])

        money_spent += money

    return money_spent
