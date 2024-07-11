''' definitions for fairness metrics '''
import networkx as nx
import numpy as np

''' average number of triangles each refugee is in'''
def triangles(G):
    new_nodes = [x for x in list(G.nodes()) if G.nodes[x]['arrived'] != 0]

    triangles = nx.triangles(G, new_nodes)
    tri_list = list(triangles.values())

    avg_tri = 0 if len(tri_list) == 0 else np.mean(tri_list)
    max_tri = ((G.number_of_nodes()-1)*(G.number_of_nodes()-2))/2

    norm_tri = avg_tri/max_tri

    return norm_tri
