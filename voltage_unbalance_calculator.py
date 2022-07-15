

import csv
import pandas as pd
import numpy as np


# load 3 csv files (delete comments before label row and # before labels)
csv_A = pd.read_csv('node_A.csv')
csv_B = pd.read_csv('node_B.csv')
csv_C = pd.read_csv('node_C.csv')

# print(type(csv_A))

# check if csv files can be merged (do they have the same timestamps?)
if not (csv_A['timestamp'].equals(csv_B['timestamp']) and csv_A['timestamp'].equals(csv_C['timestamp'])):
    raise Exception("csv files do not match")

# ---------------------- variables -------------------------

# list to store timestamps in order: ['2000-01-01 00:00:00 PST', '2000-01-01 01:00:00 PST', ...]
timestamp_list = csv_A['timestamp'].to_list()
# dictionary to store timestamps 
timestamp_dict = dict.fromkeys(timestamp_list,0)
nodes = list(csv_A.columns)[1:] # list of all nodes 
nodes_dict = dict.fromkeys(nodes,0)
voltage_unbalances = dict.fromkeys(tuple(nodes), timestamp_dict) # dictionary to store voltage unbalances for each node at each timestep

nested = [] # stores phase voltages for all nodes
nested_node = [] # stores phase voltages for one node
matA = np.array([1, 1, 1, 1, (-0.5-0.866j), (-0.5+0.866j), 1, (-0.5+0.866j), (-0.5-0.866j)]).reshape(3,3) # matrix used to calculate sequence voltages 
matA_inv = np.linalg.inv(matA)
# build nested list of phase voltages
csv_A = csv_A.drop(['timestamp'], axis=1) # drop 'timestamp' column from dataframe 
for node in csv_A: 
    for index in csv_A.index:
        phase_A = complex(csv_A[node][index].replace('i', 'j')) # convert to complex number
        phase_B = complex(csv_B[node][index].replace('i', 'j')) # convert to complex number
        phase_C = complex(csv_C[node][index].replace('i', 'j')) # convert to complex number
        phase_voltages = [phase_A, phase_B, phase_C]
        nested_node.append(phase_voltages)
    nested.append(nested_node) # add individual node's phase voltages to general nested list
#    print(len(nested_node))
    nested_node = [] # reset after appending 

node_index = 0
time_index = 0

# -------------------- matrix multiplication ---------------------
for node in nested: # node is a list of phase voltages at different timesteps 
    for voltages in node:
        voltages = np.array(voltages)
        Vs = np.matmul(matA_inv, voltages.reshape(3,1))
        if abs(Vs[2].item()/Vs[1].item()) > 0.02:
            nodes_dict[nodes[node_index]] += 1
            print(nodes[node_index])
            #voltage_unbalances[nodes[node_index]][timestamp_list[time_index]] += 1
            #print(voltage_unbalances[nodes[node_index]][timestamp_list[time_index]])
           # print('true')
           #voltage_unbalances[nodes[node_index]][timestamp_list[time_index]] += 0
           
       # time_index += 1
    #time_index = 0
    node_index += 1

print(nodes_dict)