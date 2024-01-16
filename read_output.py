from json import JSONEncoder
import json
import plotting
import numpy as np

N = 50
ntwk_iters = 10

rho_list = [5,10]
Tau_list = [(2,10),(2,2)]
new_rho_list = [x/N+ntwk_iters for x in rho_list]

filename = 'sim_output/rq2.json'

# Deserialization
with open(filename, "r") as read_file:
    decodedArray = json.load(read_file)

    arr1 = np.asarray(decodedArray["triangles"])
    arr2 = np.asarray(decodedArray["amount_spent"])

plotting.heat_map(arr1, new_rho_list, Tau_list, type = 'triangles', title = 'test1', save = True)
plotting.heat_map(arr2, new_rho_list, Tau_list, type = 'num_prop', title = 'test2', save = True)
