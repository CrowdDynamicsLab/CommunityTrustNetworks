from json import JSONEncoder
import json
import plotting
import numpy as np
import pandas as pd

N = 100
ntwk_iters = 15

rho_list = [0, 5, 10, 15, 20]
Tau_list = [(2,20),(2,10),(2,5),(2,2),(5,2),(10,2),(20,2)]
new_rho_list = [x/(ntwk_iters) for x in rho_list]
new_Tau_list = [np.round((a)/(a+b),2) for (a,b) in Tau_list]


filenames = ['sim_output_new/rq2_1fifth_new10.json', 'sim_output_new/rq2_2fifth_new10.json', 'sim_output_new/rq2_3fifth_new10.json', 'sim_output_new/rq2_4fifth_new10.json', 'sim_output_new/rq2_5fifth_new10.json' ]

arr_list1 = np.empty((5,len(rho_list), len(Tau_list), 10))
arr_list2 = np.empty((5,len(rho_list), len(Tau_list), 10))
arr_list3 = np.empty((5,len(rho_list), len(Tau_list), 10))

#filename = 'sim_output_new/rq3_local_new10.json'

# Deserialization
for idx, filename in enumerate(filenames):
    with open(filename, "r") as read_file:
        decodedArray = json.load(read_file)

        arr1 = np.asarray(decodedArray["triangles"])
        arr2 = np.asarray(decodedArray["new_trust"])
        arr3 = np.asarray(decodedArray["amount_spent"])

    arr_list1[idx] = arr1
    arr_list2[idx] = arr2
    arr_list3[idx] = arr3

#plotting.heat_map(arr1, new_rho_list, new_Tau_list, type = 'triangles', title = 'rq3_local_new10_triangles', save = True)
#plotting.heat_map(arr2, new_rho_list, new_Tau_list, type = 'apl', title = 'rq3_local_new10_trust', save = True)
#plotting.heat_map(arr3, new_rho_list, Tau_list, type = 'spent', title = 'rq2_5fifth_new10_spent', save = True)

#plotting.surface_plot(arr1, new_rho_list, new_Tau_list, type = 'triangles', title = 'rq1_new10_triangles_surface', save = True)

plotting.stacked_lines(arr_list1, new_rho_list, new_Tau_list, title = 'rq2_new10_triangles_lines', type = 'triangles', save = True)
plotting.stacked_lines(arr_list2, new_rho_list, new_Tau_list, title = 'rq2_new10_trust_lines', type = 'new_trust', save = True)
plotting.stacked_lines(arr_list3, new_rho_list, new_Tau_list, title = 'rq2_new10_spent_lines', type = 'spent', save = True)
