''' definitions for fairness metrics '''
import networkx as nx

def connectedness(G):
    return nx.edge_connectivity(G)

def apl(G):
    apl = 0
    num_comp = 0
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        if C.number_of_nodes() != 1:
            apl += (nx.average_shortest_path_length(C))
            num_comp += 1
    apl = apl/num_comp
    return 1/apl

# TODO: think of better metrics
