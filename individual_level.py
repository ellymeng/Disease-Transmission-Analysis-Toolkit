import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.linalg as ln
from openpyxl import Workbook
import xlsxwriter as xlsx
import pickle


############## Read data and convert to dictionary ###############################################

data_list=['conference','hospital','primary_school','workplace','high_school']


for data in data_list:
    original_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID1','ID2','start_time','end_time'])
    reverse_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID2','ID1','start_time','end_time'])
    df=pd.concat([original_df,reverse_df])

    ID_list=list(set(df['ID1'])) # if node = letter, set() prints list in diff order each time
    # print(ID_list)

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

    pickle.dump(ID_list, open('../Ellys_pickles/'+data+'/ID_list.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

    ################################## degree ######################################

    degree={}
    for node in ID_list:
        neighbors=[]
        for item in contacts_dict[node]:
            if item[0] not in neighbors:
                neighbors.append(item[0])
        degree[node]=len(neighbors)

    pickle.dump(degree, open('../Ellys_pickles/'+data+'/degree.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


    ###################### number of interactions #################################

    interactions={}
    for node in ID_list:
        interactions[node]=len(contacts_dict[node])

    pickle.dump(interactions, open('../Ellys_pickles/'+data+'/interactions.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


    ###################### duration of interactions #################################

    duration={}
    for node in ID_list:
        dur_interaction=0
        for item in contacts_dict[node]:
            dur_interaction+=item[2]-item[1]
        duration[node]=dur_interaction

    pickle.dump(duration, open('../Ellys_pickles/'+data+'/duration.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


