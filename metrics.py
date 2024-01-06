''' definitions for fairness metrics '''
import networkx as nx
import numpy as np

''' average number of triangles each refugee is in'''
def triangles(G):
    new_nodes = [x for x in list(G.nodes()) if G.nodes[x]['arrived'] != 0]

    triangles = nx.triangles(G, new_nodes)
    tri_list = list(triangles.values())

    avg_tri = 0 if len(tri_list) == 0 else np.mean(tri_list)
    max_tri = (G.number_of_nodes()-1)*(G.number_of_nodes()-2)

    norm_tri = avg_tri/max_tri

    return norm_tri

''' simple connectivity '''
def connectedness(G):
    return nx.edge_connectivity(G)

''' average shortest path length in each connected component '''
def apl(G):
    apl = 0
    num_comp = 0
    for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        if C.number_of_nodes() != 1:
            apl += (nx.average_shortest_path_length(C))
            num_comp += 1
    apl = apl/num_comp
    return 1/apl

''' average number of triangles each refugee is in with non refugees '''
def old_triangles(G):

    new_nodes = [x for x in list(G.nodes()) if G.nodes[x]['arrived'] != 0]

    num_tri = {key: 0 for key in new_nodes}

    triangles = [tri for tri in nx.enumerate_all_cliques(G) if len(tri) == 3]

    for triangle in triangles:

        a = triangle[0]
        b = triangle[1]
        c = triangle[2]

        # find out if each node is in V_new
        a_ref = False if G.nodes[a]['arrived'] == 0 else True
        b_ref = False if G.nodes[b]['arrived'] == 0 else True
        c_ref = False if G.nodes[c]['arrived'] == 0 else True

        # check for a
        if a_ref:
            if not b_ref or not c_ref:
                num_tri[a] += 1

        # check for b
        if b_ref:
            if not a_ref or not c_ref:
                num_tri[b] += 1

        # check for c
        if c_ref:
            if not b_ref or not a_ref:
                num_tri[c] += 1

    tri_list = list(num_tri.values())
    avg_tri = 0 if len(tri_list) ==0 else np.mean(tri_list)

    # normalize by max possible triangles for a ref to have
    num_old_nodes = G.number_of_nodes() - len(new_nodes)
    max_tri_1 = num_old_nodes * len(new_nodes)
    max_tri_2 = num_old_nodes * (num_old_nodes - 1)
    max_tri = max_tri_1 + max_tri_2

    norm_tri = avg_tri/max_tri

    return norm_tri
