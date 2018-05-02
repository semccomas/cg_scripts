import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

system = 'POPC.POPE.POPS.POSM.POPA.EQUAL'
i_o = 'OUT'
trajdir = '/data2/coarse_graining/' + system + "/" + i_o + '/analysis/'
print 'trajdir ', trajdir


popc = np.load(trajdir + 'resid_tmax.POPC.npy')
pope = np.load(trajdir + 'resid_tmax.POPE.npy')
pops = np.load(trajdir + 'resid_tmax.POPS.npy')
popa = np.load(trajdir + 'resid_tmax.POPA.npy')
posm = np.load(trajdir + 'resid_tmax.POSM.npy')


#BOXPLOTS
popc_sort = np.sort(popc[:,1])
pope_sort = np.sort(pope[:,1])
pops_sort = np.sort(pops[:,1])
popa_sort = np.sort(popa[:,1])
posm_sort = np.sort(posm[:,1])

fig, ax = plt.subplots()
labelgroup = ['POPC', 'POPE', 'POPS', 'POPA', 'POSM']
data = [popc, pope, pops, popa, posm]

data_sort = [popc_sort, pope_sort, pops_sort, popa_sort, posm_sort]
a = ax.boxplot(data_sort)#, whis = 3)   #whis = 3 will extend whiskers 
ax.set_xticklabels(labelgroup)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.set_ylabel('# ns Tmax')
plt.title(system + ' ' + i_o)
plt.savefig(trajdir + 'boxplot.png')


dct_outliers = {}


for lipid, name in enumerate(labelgroup):   #take the position of the labelgroup, the name we don't care about
    outliers_list = a['fliers'][lipid].get_data()[1]      #this accesses the y value for the outliers in the plots
    garbage = []   #garbage is only to make our life easier because when you check the outliers in the array, if there are more than one matching value it will be printed out too        
    dct_outliers['outliers_%s' % name] = {}
    for tmax_outlier in outliers_list:    #loop through each outlier in the list 
        garbage.append(list(data[lipid][:,0][data[lipid][:,1] == tmax_outlier]))   #get the list of residues corresponding to these values
    for residue in garbage:        
        for index in range(len(residue)):    #need to loop through in case there are multiple values , see above
            dct_outliers['outliers_%s' % name][residue[index]] = data[lipid][int(residue[index] - 1)][1]   #make a dictionary with the values , we do val[residue - 1] for indexing reasons


df = pd.DataFrame(dct_outliers)
#if you want a dataframe, it can be useful here













'''
plt.bar(popc[:,0], popc[:,1], width = 0.6, color = 'blue', label = 'POPC')
plt.bar(pope[:,0]+0.6, pope[:,1], width = 0.6, color = 'orange', label = 'POPE')
plt.bar(pops[:,0]+1.2,pops[:,1], width = 0.6, color = 'green', label = 'POPS')
plt.xlim(0, np.max(popc[:,0]))
plt.legend()
plt.show()



dct_outliers = {}
for index, name in enumerate(labelgroup):
	outliers_values = a['fliers'][index].get_data()[1]  #this accesses the outliers from the plot
	dct_outliers['outliers_%s' % name] = []   #create a dictionary of lists, below we will add the outliers to the list
	for val in outliers_values:
			#print data[index][np.where(data[index][:,1] == val)]    #data and labelgroup are the same order, so you can access the index the same way
			dct_outliers['outliers_%s' % name].append(data[index][np.where(data[index][:,1] == val)])   #append to your created list




'''