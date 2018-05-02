import numpy as np
import matplotlib.pyplot as plt

trajdir = '/data2/coarse_graining/POPC.POPE.POPS.POSM.POPA/IN/analysis/'

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

data = [popc_sort, pope_sort, pops_sort, popa_sort, posm_sort]
ax.boxplot(data, whis =5)   #whis = 3 will extend whiskers 
ax.set_xticklabels(['POPC', 'POPE', 'POPS', 'POPA', 'POSM'])
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.show()










'''
plt.bar(popc[:,0], popc[:,1], width = 0.6, color = 'blue', label = 'POPC')
plt.bar(pope[:,0]+0.6, pope[:,1], width = 0.6, color = 'orange', label = 'POPE')
plt.bar(pops[:,0]+1.2,pops[:,1], width = 0.6, color = 'green', label = 'POPS')
plt.xlim(0, np.max(popc[:,0]))
plt.legend()
plt.show()
'''