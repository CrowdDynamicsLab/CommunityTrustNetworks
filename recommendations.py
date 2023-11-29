''' code for public entity to make recommendations'''

import random

def agent_selection(G, rho):
    ''' choose rho many agents to give recs to '''

    return random.choices(list(G.nodes()), k = rho)

def recommend(G, agents):
    ''' return the recs for the chosen agents as a dict '''

    recs = {key: None for key in list(G.nodes())}
    for node in agents:
        recs[node] = random.choice([x for x in list(G.nodes()) if x != node])
    return recs
