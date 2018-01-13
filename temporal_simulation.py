import numpy as np
import random
import time as tm

def get_infection_tree(seed,contacts,time,params):
    #print()
    ID_list=list(set(contacts.keys()))
    N=len(ID_list)   
    time_of_infection={}
    source_of_infection={seed:None}
    
    #make a proportion of the nodes asymptomatic
    asymptomatic_nodes=random.sample(ID_list,int(N*params['asymptomatic_proportion']))

    #infection_tree is the tree network of infections that the function returns
    infection_tree=[]    
    #keep a list of infected nodes (at the beginning it contains only 'node')    
    immune_nodes=[seed]
    infections=[[seed,time]]
    infectious_node=seed
    
    #choose the shape and scale of the gamma distribution
    offset=max(0,params['l_mode']-5*params['l_sigma'])
    if offset>0:
        k=1+5**2
        theta=params['l_sigma']/5
    else:
        x=(params['l_mode']/params['l_sigma'])**2
        k=1+(x/2)+(np.sqrt(x*(2+x)))/2            
        theta=(params['l_sigma']**2)/params['l_mode']    

    while len(infections)>0:

        #randomly select a latent duration 
        if infectious_node==seed:
            latent_duration=0
        else:
            latent_duration=int(60*60*(offset+np.random.gamma(k,theta)))
        #randomly select an infectious duration 
        if infectious_node in asymptomatic_nodes:
            infectious_duration=5*24*60*60
        else:
            infectious_duration=int(60*60*np.random.gamma(params['i_shape'], scale=params['i_mode']/(params['i_shape']-1)))
  
            
        #loop over all the potentially infectious interactions
        for contact in contacts[infectious_node]:
            name=contact[0]
            contact_start=contact[1]
            contact_end=contact[2]
            #check that the interaction is with a susceptible node
            if name not in immune_nodes: 
                #the susceptible node is exposed to the infection between eposure_start and exposure_end
                #exposure starts either at the start of infectious period or the start of interaction, whichever is later
                exposure_start=max(time+latent_duration,contact_start)
                #exposure endes at the end of infectious period or the end of interaction, whichever is earlier
                exposure_end=min(time+latent_duration+infectious_duration,contact_end)
                #check that it was a potentially infectious contact              
                if exposure_end>exposure_start:
                    #select a random time for the infection to occur
                    r=random.random()
                    #this is equivalent to an attempt at transmission occuring each second
                    l=-np.log(1-params['beta'])                                
                    infection_time=exposure_start+int(-(1/l)*np.log(1-r))             
                    
                    if infection_time<exposure_end:
                        #if this is the case then a potential infection occurs!
                                                
                        #if this is the first time 'name' has been infected then add it to the list
                        if name not in time_of_infection:
                            #keep track of the time of the infection
                            time_of_infection[name]=infection_time
                            #keep track of where it came from
                            source_of_infection[name]=infectious_node
                            #update the list
                            infections.append([name,infection_time])
                        #if this is  an earlier infection time for 'name' then replace
                        elif infection_time<time_of_infection[name]:
                            #remove the later infection time
                            infections.remove([name,time_of_infection[name]])
                            #add the earlier infection time
                            infections.append([name,infection_time])
                            #keep track of where it came from
                            source_of_infection[name]=infectious_node
                            #update the list
                            time_of_infection[name]=infection_time


        #get earliest infection event on the list
        next_infection=min(infections,key=lambda x: x[1])        
        #remove the chosen infection
        infections.remove(next_infection)
        
        infectious_node=next_infection[0]
        #add it to the immune list
        immune_nodes.append(infectious_node)        
        #update the time
        time=next_infection[1]
        
        #add to the tree
        infection_tree.append(next_infection+[source_of_infection[next_infection[0]]])

    return infection_tree
    
