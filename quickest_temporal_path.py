import sys
sys.path.append("../")
import pandas as pd
import xlsxwriter as xlsx
import pickle
    
    
def path_end_time(i,j,t):
    # If I leave i after time t, whats earliest I can get to j?

    # first make sure bst(i,j,t) has not already been calculated
    if (i,j,t) not in earliest_end_times:
        # the sp between i and itself is t 
        if i==j:
            earliest_end_times[(i,j,t)]=t # base case
        else:
            # if there is no path then bst(i,j,t) needs to occur before any other interaction
            earliest_end_time=10**10     # ** = exponentiation       
            # loop over all the edges that arrive at j 
            #temp_df=df[(df['ID2']==j)&(df['end_time']<t)]
            for contact in contacts_dict[i]:
                if contact[1]>t:
            #for x,row in temp_df.iterrows():
                # compute the best start time for paths that arrive at the current contact (before it ends)
                # new_time=path_start_time(i,row['ID1'],row['end_time'])
                    new_time=path_end_time(contact[0],j,contact[1])
                # if the end time is earlier than the "best_start_time" variable, update
                    if new_time<earliest_end_time:
                        earliest_end_time=new_time
            # after the loop we have the latest possible start time to arrive before time t
            earliest_end_times[(i,j,t)]=earliest_end_time
    return earliest_end_times[(i,j,t)]


data_list=['conference','hospital','primary_school','workplace','high_school']
# data_list=['hospital']

for data in data_list:
    
    ############## Read the data ###############################################
    # First read the data as normal,
    original_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID1','ID2','start_time','end_time'])
    # then read it again but with the column names switched around,
    reverse_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID2','ID1','start_time','end_time'])
    # then concatenate the two dataframes together so that all the interactions are in one dataframe.
    df=pd.concat([original_df,reverse_df])      
    # sort it into chronological order
    df=df.sort_values('start_time')
    #Get a list of all the nodes
    ID_list=list(set(df['ID1']))

    ############# Change the format of the data #################################

    # We will create a dictionary of lists of lists. This is essentially what an "adjacency 
    # list" is. For every node in the network we have a list of all the other nodes it interacted 
    # and at what time. We start with an empty dictionary,
    contacts_dict={}
    # and add these lists one node at a time
    for node in ID_list:
        # First, use the dataframe to get all the interactions involving the node 
        node_df=df[(df['ID1']==node)] #mine
        # Then turn the ID2 column into a list 
        names=node_df['ID2'].tolist()
        # do the same for the start and end times
        start_times=node_df['start_time'].tolist()
        end_times=node_df['end_time'].tolist()
        # the adjacency list starts as an empty list, 
        contacts_dict[node]=[]
        # then we add things to it one by one
        for i in range(len(names)):
            # each element in the list contains exactly 3 things: the name of ID2, the start_time 
            # and the end_time
            contacts_dict[node].append([names[i],start_times[i],end_times[i]])


    ############# Compute temporal closeness of each node ###########################

    earliest_end_times={}
    temporal_closeness={}
    # find the start time of the sample
    start_time=min(df['start_time'])
    # loop over every ordered pair of nodes
    n=1    
    for i in ID_list:
        print(n,'of',i)
        n=n+1
        closeness=0
        for j in ID_list:
            if i==j:
                qp=0
            else:
                path_durations=[]
                # loop over all the paths that start at i,  
                for contact in contacts_dict[i]:
                    # calculate the duration of the path that goes through each contact (earliest_end_time - start_time)
                    path_durations.append(1+path_end_time(contact[0],j,contact[1])-contact[1])
                # find the one with the shortest duration (earliest_end_time - start_time)
                qp=min(path_durations)
                # print('qp = ',qp)
                closeness=closeness+(1/qp)
        temporal_closeness[i]=(closeness)

    pickle.dump(temporal_closeness, open('../Ellys_pickles/'+data+'/quickest_temporal_path.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
                    



       