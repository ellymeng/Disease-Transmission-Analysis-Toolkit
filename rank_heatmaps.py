import sys
sys.path.append("../")
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import pickle

def get_rank(centralities):
    # get the length of the list
    centralities = list(centralities.values())
    N=len(centralities) 
    # we can see that node 0 is ranked first, node 3 is ranked second, 1 is third and 2 is fourth
    # the goal is to make python do the ranking for us
    # then we add the node names 
    centrality_names = [[i,centralities[i]] for i in range(N)]
    # you can print this so you can see what the list looks like  
    # print(centrality_names)
    # print()
    # then we sort it according to the value of the second entry in each mini-list
    centrality_ordered=sorted(centrality_names, key=lambda item: item[1], reverse=True)
    # print this to see what it looks like    
    # print(centrality_ordered)
    # print()
    # then output the ranks of all the individuals 
    # we start with a list of 0s
    centrality_rank=[0]*N
    # loop through the nodes
    for i in range(N):
        # find the node in the ith position
        a=centrality_ordered[i]
        # the rank of that node is i
        centrality_rank[a[0]]=i

    return centrality_rank

# Plot the results of the centralities table that you have created. For example 
# suppose that we had only three centralities to compare and the table looked
# like 
#
#  __\__A__\__B__\__C__
#  A \  1  \ 0.6 \ 0.9
#  B \ 0.7 \  1  \ 0.8
#  C \ 0.6 \ 0.7 \  1
#
# then we represent it as a matrix using numpy

# values=np.array([[1,0.6,0.9],[0.7,1,0.8],[0.6,0.7,1]])
# print(values)

data_list=['conference','hospital','primary_school','workplace','high_school']

# data_list=['conference','hospital','primary_school','workplace']

for data in data_list:
    
    ID_list=pickle.load(open('../Ellys_pickles/'+data+'/ID_list.pickle', 'rb'))    
    # sim = pickle.load(open('../Ellys_pickles/'+data+'/degree.pickle','rb'))
    deg = pickle.load(open('../Ellys_pickles/'+data+'/degree.pickle', 'rb'))
    num_inter = pickle.load(open('../Ellys_pickles/'+data+'/interactions.pickle', 'rb'))
    dur_inter = pickle.load(open('../Ellys_pickles/'+data+'/duration.pickle', 'rb'))
    nxcs = pickle.load(open('../Ellys_pickles/'+data+'/closeness.pickle','rb'))
    katz = pickle.load(open('../Ellys_pickles/'+data+'/katz.pickle', 'rb'))
    bet = pickle.load(open('../Ellys_pickles/'+data+'/betweenness.pickle', 'rb'))
    com = pickle.load(open('../Ellys_pickles/'+data+'/communicability.pickle', 'rb'))
    cs = pickle.load(open('../Ellys_pickles/'+data+'shortest_temporal_path.pickle','rb'))
    ct = pickle.load(open('../Ellys_pickles/'+data+'/quickest_temporal_path.pickle','rb'))
    eig = pickle.load(open('../Ellys_pickles/'+data+'/eigenvector.pickle','rb'))

    # cw = pickle.load(open('../pickled_files/'+data+'/'+data+'_networkx_cc_weighted.pickle','rb'))


    # rank_sim = get_rank(sim)
    rank_deg = get_rank(deg)
    rank_num_inter = get_rank(num_inter)
    rank_dur_inter = get_rank(dur_inter)
    rank_nxcs = get_rank(nxcs)
    rank_katz = get_rank(katz)
    # rank_cw = get_rank(cw)
    rank_bet = get_rank(bet)
    rank_com = get_rank(com)
    rank_cs = get_rank(cs)
    rank_ct = get_rank(ct)
    rank_eig = get_rank(ct)

    all_ranks = [rank_deg,rank_num_inter,rank_dur_inter,rank_nxcs,rank_katz,rank_bet,rank_com,rank_cs,rank_ct,rank_eig]
     
    rows=[]
    for item1 in all_ranks:
    	row=[]
    	for item2 in all_ranks:
    		r,p=st.spearmanr(item1,item2)
    		row.append(r)
    	rows.append(row) 

    arr=[]
    for i in range(len(all_ranks)):
    	arr.append(rows[i])   

    values=np.array(arr)
    print(values)

    plt.figure()
    plt.title('Centrality Ranks Comparison', fontsize=10)
    x = y = np.array([0,1,2,3,4,5,6,7,8,9,10])
    my_xticks = my_yticks = ['deg','num','dur','cs','nxcs','ct','bet','katz','com','eig']
    plt.xticks(x, my_xticks, fontsize=7.5)
    plt.yticks(y, my_yticks, fontsize=7.5)
    plt.imshow(values,interpolation='none',cmap='Greys') # displays in color
    plt.colorbar()

    plt.savefig(data+'_rank_table.png',format='png')



