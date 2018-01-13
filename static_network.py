import sys
sys.path.append("../")
import numpy as np
import pandas as pd
import networkx as nx
import pickle


# katz centrlaity: computes the relative influence of a node by measuring the number of 
# immediate neighbors (first degree nodes) and also all other nodes that 
# connect to the node under consideration through these immediate neighbors

data_list=['conference','hospital','primary_school','workplace','high_school']

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


#make the graph
    G=nx.Graph()
    edges=[]
    for i,row in df.iterrows():
        edge=sorted([row['ID1'],row['ID2']])
        
        if edge not in edges:
            w=len(df[(df['ID1']==row['ID1'])&(df['ID2']==row['ID2'])])+len(df[(df['ID1']==row['ID2'])&(df['ID2']==row['ID1'])])
            edges.append(edge)

            G.add_edge(row['ID1'], row['ID2'], weight=1)

    #################### closenes centrality using nx ######################

    closeness=nx.closeness_centrality(G)
#
    pickle.dump(closeness, open('../Ellys_pickles/'+data+'/closeness.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
#
#
#    #################### katz centrality using nx without edge weights ######################

    katz=nx.katz_centrality(G,alpha=0.005)

    pickle.dump(katz, open('../Ellys_pickles/'+data+'/katz.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    print(katz)
#
#    ########################### betweenness centrality ############################
#
    # ratio of how often a node was traversed to the total number of shortest paths

    betweenness=nx.betweenness_centrality(G)

    pickle.dump(betweenness, open('../Ellys_pickles/'+data+'/betweenness.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

#    ########################### eigenvector centrality ############################
#
    # measure of a node's importance based on how well it is linked to important neighbors

    eigenvector=nx.eigenvector_centrality_numpy(G)

    pickle.dump(eigenvector, open('../Ellys_pickles/'+data+'/eigenvector.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

