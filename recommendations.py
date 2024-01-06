''' code for public entity to make recommendations'''

import random
import metrics

def agent_selection(G, rho, it):
    ''' choose rho many agents to give recs to '''

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

    return ranked_agents[:rho]

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
