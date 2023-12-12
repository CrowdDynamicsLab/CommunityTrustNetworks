''' definitions for fairness metrics '''
import networkx as nx

def connectedness(G):
    return nx.edge_connectivity(G)

def apl(G):
    apl = 0
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        apl += (nx.average_shortest_path_length(C))
    return 1/apl

# TODO: think of better metrics for disconnected graphs 
