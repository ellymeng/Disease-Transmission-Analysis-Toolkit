#This first couple of lines allows us to imprt things from the parent folder
import sys
sys.path.append("../")
# We need to import the other puthon file "temporal_simulatio.py" that does the simulation.
import temporal_simulation as ts
import pandas as pd
import scipy.stats as st
import random
import pickle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import timeit

data_list=['conference','workplace','hospital','high_school','primary_school']
total_days={'hospital':4,'conference':3,'high_school':5,'primary_school':2, 'workplace':11}
data_list=['high_school']


for data in data_list:

    # read the data
    original_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID1','ID2','start_time','end_time'])
    # read it again with edge directions reversed (so that the disease can go in both directions)
    reverse_df=pd.read_csv('../data/'+data+'.txt', sep='\t', header=None, names=['ID2','ID1','start_time','end_time'])
    #put them together
    df=pd.concat([original_df,reverse_df])

    # this part loops the data so that the 4 days repeats itself as soon as it ends
    shifted_df={}
    old_start=df['start_time'].tolist()
    old_end=df['end_time'].tolist()

    # create 5 dataframes identical to the original except time stamps are shifted
    # by 4,8,12,16,20 days  
    for n in range(5):
        new_start=[t+(n*total_days[data]*24*60*60) for t in old_start]
        new_end=[t+(n*total_days[data]*24*60*60) for t in old_end]
        shifted_df[n]=df.copy()
    #    shifted_df[n]=shifted_df[n].reset_index(drop=True)
        shifted_df[n]['start_time']=new_start
        shifted_df[n]['end_time']=new_end
    # put all the shifted dataframes together
    looped_df=pd.concat([shifted_df[n] for n in shifted_df])

    # get list of all node names 
    ID_list=list(set(df['ID1']))

    # This part creates contact lists for every node (this is the best way to format
    # for the simulation the data)
    contacts_dict={}
    for node in ID_list:
        node_df=looped_df[(looped_df['ID1']==node)]
        names=node_df['ID2'].tolist()
        start_times=node_df['start_time'].tolist()
        end_times=node_df['end_time'].tolist()
        contacts_dict[node]=[]
        for i in range(len(names)):
            contacts_dict[node].append([names[i],start_times[i],end_times[i]])

    ###############################################################################################

    start_time = timeit.timeit()

    # default: b = 0.00015, imode = lmode = 24
    beta_values=[0.00005*n for n in range(1,11)]
    beta=0.00045
    i_mode_values=[4*n for n in range(1,11)]
    i_mode=12 # increasing this causes sim time for workplae to increase up to 7-9s
    l_mode_values=[4*n for n in range(1,11)]
    l_mode=40

    # for l_mode in l_mode_values:
        # print('l_mode: ',l_mode)

    # move everything below one tab right when done with task 3
    print('parameters: ',beta,i_mode,l_mode)

    parameters={'beta':beta, # this is the transmission probability
         'i_mode':i_mode, # this corresponds to the infectious period (in hours)
         'i_shape':1.5, # don't worry about this one for now 
         'l_sigma':2, # or this one 
         'l_mode':l_mode, # this corresponds to the latent period (in hours)
         'asymptomatic_proportion':0, # ignore these last two for now
         'immune_proportion':0} 

    # we want to know the proportion of times each node receives the infection
    times_infected={}
    times_infected_list=[]

    for node in ID_list:
        times_infected[node]=0

    outbreak_sizes=[]
    # we take the average over T of smulations. T should be large (10,000)    
    T=1000
    for i in range(T):
        # choose a random node to be the seed
        seed=ID_list[int(len(ID_list)*random.random())]
        # choose a random time
        time=min(df['start_time'])+int(5*24*60*60*random.random())
        # this line runs the disease simulation
        tree=ts.get_infection_tree(seed,contacts_dict,time,parameters)
        # now update the totals
        for node in [t[0] for t in tree]:
            # if it is infected add 1/T (which is the same as adding 1 and then 
            # dividing by T at the end)
            times_infected[node]+=(1/T)

        # outbreak_sizes.append(len(tree))

    end_time = timeit.timeit()
    print('time simulation took: ',end_time - start_time,len(tree))
    
    # filename='../Ellys_pickles/'+data+'/simulation/sim_'+str(beta)+'_'+str(i_mode)+'_'+str(l_mode)+'.pickle'
    # pickle.dump(times_infected, open(filename, 'wb'))

    