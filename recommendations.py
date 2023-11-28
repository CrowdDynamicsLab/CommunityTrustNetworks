''' code for public entity to make recommendations'''

def agent_selection(G, rho):
    ''' choose rho many agents to give recs to '''

    return list(G.nodes())[:rho]

def recommend(G, agents):
    ''' return the recs for the chosen agents as a dict '''

    recs = {key: None for key in list(G.nodes())}
    return recs
