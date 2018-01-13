import matplotlib.pyplot as plt
import pickle
import scipy.stats as st
import numpy as np

data_list=['conference','hospital','primary_school','workplace','high_school']


for data in data_list:

    print(data,"===========================================")

    beta_values=[0.00005*n for n in range(1,11)]
    beta=0.00015
    i_mode_values=[4*n for n in range(1,11)]
    i_mode=24
    l_mode_values=[4*n for n in range(1,11)]
    l_mode=24

    centrality_measures=['degree','interactions','duration','closeness','katz','betweenness','eigenvector','communicability','quickest_temporal_path','shortest_temporal_path']

    ID_list=pickle.load(open('../Ellys_pickles/'+data+'/ID_list.pickle', 'rb'))
    # print(ID_list)

    mean_corr_figure = []
    for c in centrality_measures:    
        centrality=pickle.load(open('../Ellys_pickles/'+data+'/'+c+'.pickle', 'rb'))
        # print(c)
        # print(len(centrality))
        
        correlation=[]
        for l_mode in l_mode_values:    
            filename='../Ellys_pickles/'+data+'/simulation/sim_'+str(beta)+'_'+str(i_mode)+'_'+str(l_mode)+'.pickle'
            infection_risk=pickle.load(open(filename,'rb'))
                 
            x=[]
            y=[]
            for node in ID_list:
                #print(centrality[node],infection_risk[node])
                x.append(centrality[node])
                y.append(infection_risk[node])
                
            spearman_test=st.spearmanr(x,y)
            correlation.append(spearman_test[0])

        # plt.plot(l_mode_values, correlation,label=c) 

        # list of mean correlations for each centrality measure for each figure
        mean_corr_figure.append(np.mean(correlation))

    # pickle.dump(mean_corr_figure, open('../Ellys_pickles/'+data+'/meancorr_fig_lmode.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

    # calculate mean correlation for each centrality measure for each dataset (i.e. the mean over all parameter combinations)
    mean_corr_dataset = []
    mean_corr_beta = pickle.load(open('../Ellys_pickles/'+data+'/meancorr_fig_beta.pickle', 'rb'))
    mean_corr_imode = pickle.load(open('../Ellys_pickles/'+data+'/meancorr_fig_imode.pickle', 'rb'))
    mean_corr_lmode = pickle.load(open('../Ellys_pickles/'+data+'/meancorr_fig_lmode.pickle', 'rb'))

    # one entry for each centrality measure in the dataset
    for i in range(len(centrality_measures)):
        mean_corr_dataset.append(np.mean([mean_corr_beta[i], mean_corr_imode[i], mean_corr_lmode[i]]))

    # print(mean_corr_dataset)
    # pickle.dump(mean_corr_dataset, open('../Ellys_pickles/'+data+'/meancorr_dataset.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


    # #plt.axis.Tick(beta_values)
    # plt.xlabel('l_mode')
    # plt.ylabel('Correlation Between Simulation and Centrality Measure')
    # plt.legend(loc=('lower right'),prop={'size': 10})
    # plt.savefig('samplefigure.png', format='png', bbox_inches='tight')
    # plt.show()


# calculate overall mean for each centraltiy measure (i.e. the mean over all parameter combinations and datasets)
mean_overall = []

for i in range(len(centrality_measures)):
    dataset_means = []
    for data in data_list:
        mean_corr_ds = pickle.load(open('../Ellys_pickles/'+data+'/meancorr_dataset.pickle', 'rb'))
        dataset_means.append(mean_corr_ds[i])

    mean_overall.append(np.mean(dataset_means))

print(mean_overall)
pickle.dump(mean_overall, open('../Ellys_pickles/overall_meancorr_per_cen.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)











