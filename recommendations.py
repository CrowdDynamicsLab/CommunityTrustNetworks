''' code for public entity to make recommendations'''

import random

def agent_selection(G, rho):
    ''' choose rho many agents to give recs to '''

    selected_agents = []
    for node in G.nodes():
        if G.nodes[node]['new']:
            selected_agents.append(node)

    selected_agents.extend(random.sample([x for x in list(G.nodes()) if x not in selected_agents], k = rho - len(selected_agents)))

    return selected_agents

def recommend(G, agents):
    ''' return the recs for the chosen agents as a dict '''

    recs = {key: None for key in list(G.nodes())}
    for node in agents:
        recs[node] = random.choice([x for x in list(G.nodes()) if x != node])
    return recs
