from json import JSONEncoder
import json
import plotting
import numpy as np

N = 100
ntwk_iters = 15

rho_list = [0, 5, 10, 15, 20]
Tau_list = [(2,20),(2,10),(2,5),(2,2),(5,2),(10,2),(20,2)]
new_rho_list = [x/(ntwk_iters) for x in rho_list]
new_Tau_list = [np.round((a)/(a+b),2) for (a,b) in Tau_list]

filename = 'sim_output/rq1_new10.json'

# Deserialization
with open(filename, "r") as read_file:
    decodedArray = json.load(read_file)

    arr1 = np.asarray(decodedArray["triangles"])
    arr2 = np.asarray(decodedArray["new_trust"])
    #arr3 = np.asarray(decodedArray["amount_spent"])

plotting.heat_map(arr1, new_rho_list, new_Tau_list, type = 'triangles', title = 'rq1_new10_triangles', save = True)
#plotting.heat_map(arr2, new_rho_list, Tau_list, type = 'apl', title = 'rq2_5fifth_new10_trust', save = True)
#plotting.heat_map(arr3, new_rho_list, Tau_list, type = 'spent', title = 'rq2_5fifth_new10_spent', save = True)

plotting.surface_plot(arr1, new_rho_list, new_Tau_list, type = 'triangles', title = 'rq1_new10_triangles_surface', save = True)
