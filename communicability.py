import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.linalg as ln
import pickle

 
data_list=['conference','hospital','primary_school','workplace','high_school']


for data in data_list:
    # read the data
    original_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID1','ID2','start_time','end_time'])
    # read it again with edge directions reversed (so that the disease can go in both directions)
    reverse_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID2','ID1','start_time','end_time'])
    df=pd.concat([original_df,reverse_df])
    # get a list of node names
    ID_list=list(set(df['ID1']))

    N=len(ID_list)
    # create a list of lists which we later turn into a matrix using the linalg library
    M=[]
    # get the total duration of all interactions combined
    total_weight=sum(df['end_time'])-sum(df['start_time'])

    for i in range(N):
        # create an empty row
        r=[]
        for j in range(N):
        	# select only the interactions between i and j
            ij_df=df[(df['ID1']==ID_list[i])&(df['ID2']==ID_list[j])]
            # get the total duration of the interaction between i and j
            weight=sum(ij_df['end_time'])-sum(ij_df['start_time'])
            r.append(weight/total_weight)
        # add the row to the matrix
        M.append(r)

    # convert this list to a matrix
    M=np.array(M)
    # print(M)
    # calculate the matrix exponential
    alpha=0.5
    M_exp=ln.expm(M*alpha)
    # print(M_exp)
    # This part calculates the row sum
    row_sum=np.sum(M_exp, axis=0)

    communicability={}
    communicability_list=[]
    for i in range(N):
        communicability[ID_list[i]]=row_sum[i]
        communicability_list.append(communicability[ID_list[i]])

    # The important part: communicability[ID] gives the communicability of the node 
    # named ID
    # for ID in ID_list:
    #     print(ID,communicability[ID])

    pickle.dump(communicability, open('../Ellys_pickles/'+data+'/communicability.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


    # Last we have the centralities that use the temporal network that we have 
    # made our own codes for.

    