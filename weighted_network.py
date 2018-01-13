import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import scipy.linalg as ln
from openpyxl import Workbook
import xlsxwriter as xlsx
import pickle


######################### Read data and convert to dictionary ####################################

data_list=['conference', 'high_school','hospital','primary_school','workplace']
# data_list=['hospital']

for data in data_list:
    
    original_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID1','ID2','start_time','end_time'])
    reverse_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID2','ID1','start_time','end_time'])
    df=pd.concat([original_df,reverse_df])

    ID_list=list(set(df['ID1']))


    contacts_dict={}
    for node in ID_list:
        # get all interactions involving the node in dataframe
        node_df=df[(df['ID1']==node)]
        # turn the ID2 column into a list 
        ID2_list=node_df['ID2'].tolist()
        # do the same for the start and end times
        start_times=node_df['start_time'].tolist()
        end_times=node_df['end_time'].tolist()
        # the adjacency list starts as an empty list, 
        contacts_dict[node]=[]
        # then add things to it one by one
        for i in range(len(ID2_list)):
            # each element in the list contains exactly 3 things: the name of ID2, the start_time and the end_time
            contacts_dict[node].append([ID2_list[i],start_times[i],end_times[i]])

    # print(contacts_dict)
    # print()

    ########################### duration of interactions weight ###############################

    # weight = 1/((total duration the pair interacted)

    G=nx.from_pandas_dataframe(df,'ID1','ID2',create_using=nx.Graph())

    node1_list=original_df['ID1'].tolist()
    node2_list=original_df['ID2'].tolist()


    all_interactions=[]
    for i in range(len(node1_list)):
        all_interactions.append([node1_list[i],node2_list[i]])

    unique_interactions=[]
    for n1,n2 in all_interactions:
        if [n1,n2] not in unique_interactions:
            if [n2,n1] not in unique_interactions:
                unique_interactions.append([n1,n2])
    # print(unique_interactions)

    edge_weight_t={}

    for n1,n2 in unique_interactions: # includes one copy of either 2,1 and 1,2
        interaction_length=0
        if len(contacts_dict[n1]) > 0 or len(contacts_dict[n2]) > 0:
            if len(contacts_dict[n1]) > 0:
                for item in contacts_dict[n1]:
                    if item[0]==n2:
                        interaction_length+=(item[2] - item[1])
            elif len(contacts_dict[n2]) > 0:
                for item in contacts_dict[n2]:
                    if item[0]==n1:
                        interaction_length+=(item[2] - item[1])

        edge_weight_t[n1,n2]=interaction_length

    print(edge_weight_t)

    ########################### weighted closeness centrality ###############################

    for n1,n2 in edge_weight_t:
        G.add_edge(n1,n2,weight=1/(edge_weight_t[n1,n2]))

    shortest_paths_weighted=[]

    for i in ID_list:
        shortest_paths=[]
        for j in ID_list:
            sp=nx.shortest_path_length(G,i,j,weight=1/(edge_weight_t[n1,n2]))
            shortest_paths.append(sp)
            # print(i,j,sp)
        node_centrality_weighted=(1/sum(shortest_paths))
        shortest_paths_weighted.append(node_centrality_weighted)

    pickle.dump(shortest_paths_weighted, open('../pickled_files/'+data+'/'+data+'_networkx_cc_weighted.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        # print(n1,n2,G_time_agg[n1][n2])







