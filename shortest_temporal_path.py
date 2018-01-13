import sys
sys.path.append("../")
import pandas as pd
import matplotlib.pyplot as plt 
import pickle 
import openpyxl as xl
from openpyxl import Workbook
import xlsxwriter as xlsx

 # Dijkstra's Algorithm: SP(i,j,t)=length of the shortest path from i to j after time t
def shortest_path(i,j,t):
    # first make sure sp(i,j,t) has not already been calculated
    if (i,j,t) not in shortest_paths:
        # the space between a node and itself is 0 
        if i==j: 
            shortest_paths[(i,j,t)]=0 # base case
        else:
            # if there is no path then sp(i,j,t) is infinite. Use a large number to represent infinity
            shortest=1000
            # loop over all the edges that arrive at j (compute path length for each edge)
            for contact in contacts_dict[i]:
                if contact[1]>t:
                    # compute the shortest path that goes through the current contact           
                    path_length=1+shortest_path(contact[0],j,contact[1])
                    # if its shorter than the "shortest" variable, update
                    if path_length<shortest:
                        shortest=path_length
                # at the end of the loop we have the shortest 
            shortest_paths[(i,j,t)]=shortest
                
    return shortest_paths[(i,j,t)]


################################### Read the data #######################################

# workbook = xlsx.Workbook('final_spreadsheet.xlsx')
data_list=['conference','hospital','primary_school','workplace','high_school']
data_list=['high_school']

for data in data_list:


    original_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID1','ID2','start_time','end_time'])
    reverse_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID2','ID1','start_time','end_time'])
    df=pd.concat([original_df,reverse_df])
    df=df.sort_values('start_time')

    # get a list of all the nodes
    ID_list=list(set(df['ID1']))

    ############# create an adjacency list of the data ##########################

    # Create a dictionary of lists of lists. For every node in the network, create a list of all the other nodes it interacted with 
    # and at what start and end time. Start with an empty dictionary, 
    contacts_dict={}
    # and then add these lists one node at a time
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




 ############# compute closeness centrality of each node ###########################

    start_time=0
    shortest_paths={}
    tsp_closeness={}
    
    
    for i in ID_list:
        closeness=0
        for j in ID_list:
            sp=shortest_path(i,j,start_time)
            if i!=j:
                closeness=closeness+1/sp
        tsp_closeness[i]=closeness
        print('closeness: ',closeness)

    pickle.dump(tsp_closeness, open('../Ellys_pickles/'+data+'/shortest_temporal_path.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)





