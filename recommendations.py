''' code for public entity to make recommendations'''

import random
import metrics

def agent_selection(G, rho, it):
    ''' choose rho many agents to give recs to '''

    selected_agents = []
    # prioritize new nodes
    for node in G.nodes():
        # only if it's not the first iter, prioritize new agents
        if it != 0:
            if G.nodes[node]['arrived'] == it:
                selected_agents.append(node)

    # prioritize new nodes
    selected_agents.extend(random.sample([x for x in list(G.nodes()) if x not in selected_agents], k = rho - len(selected_agents)))

    return selected_agents

def recommend(G, nodes, fairness_func):
    ''' return the recs for the chosen agents as a dict '''

    best_choice = None
    best_fairness = 0

    recs = {key: None for key in list(G.nodes())}
    for node in nodes:
        choices = [x for x in list(G.nodes()) if x != node and x not in G.neighbors(node)]
        for choice in choices:
            # only check an edge if it doesn't already exist
            if not G.has_edge(choice, node):
                G.add_edge(node, choice)
                fairness = fairness_func(G)
                G.remove_edge(node, choice)

                if fairness > best_fairness:
                    best_fairness = fairness
                    best_choice = choice

        recs[node] = best_choice
    return recs
