''' code to run simulation '''

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import formation, recommendations, metrics, plotting

iters = 10                  # network iters
N = 100                     # number of nodes init
alpha = .5                  # node types
Tau = np.random.uniform(0,1) # trust distribution
rho = 5                     #

G = formation.new(N, alpha, Tau)

# each iteration, a new node joins
for i in range(iters):
    # node enters
    formation.node_enters(G)

    # public entity makes rho many recommendations
    recs = recommendations.recommend(G, rho)

    # nodes form edges based on these recommendations and also network formation model
    formation.form_edges(G, recs)
