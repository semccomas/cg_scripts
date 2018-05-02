import MDAnalysis as md 
import numpy as np 
import matplotlib.pyplot as plt 
import sys

############################################################################
##################### USER DEFINED VARIABLES ################################
###########################################################################

lipid = sys.argv[1]
wdir = sys.argv[2]
gro = sys.argv[3]
xtc = sys.argv[4]
trajdir = wdir + '/production/'
outdir = wdir + '/analysis'
system=md.Universe(trajdir + gro , trajdir + xtc)
length_of_long_occ = 30  ### = how many nanoseconds of continuous time is 'long', so you can compare tmax with how many other times the residue is occupied for a sig amount of time

print 
print 
print 'using trajdir ' , trajdir
print
print

##############################################################################
########################### PARSING  #######################################
#############################################################################

prot = system.select_atoms('name BB') #one per residue, should be the whole protein 
pope_resids = []  #actual information per frame of each resid at the frame contacting the lipid
for ts in system.trajectory:
	pope_resids.append((system.trajectory.time, system.select_atoms('name BB SC1 SC2 SC3 SC4 and around 6 resname %s' %lipid).resids)) 

resid_tmax = np.zeros((len(prot.residues), 2))                #these are the two arrays we will append into
resid_long_occupancy = np.zeros((len(prot.residues), 2))

for n, row in enumerate(resid_tmax):
    resid = n + 1
    c = 0
    c_list = []
    for linenum, info in enumerate(pope_resids):
        if resid in info[1]:         #find where the resid is, then below we will see if it's in the next row
            try:
                if resid in pope_resids[linenum+1][1]: #same as info[1] for the next line
                    c = c + 1
                else:
                    c_list.append(c) 		# when you break the pattern, add the final value to the list, could do it above too but this makes c_list shorter
                    c = 0      				#restart count when you break the pattern
            except:
                IndexError
                pass
    if not c_list:    #can't get max of c list if c list is empty, thats why fill it with 0 above
        c_list.append(0)
    resid_tmax[n] = (resid, max(c_list))   
    long_occ_count = 0
    for count in c_list:
        if count >= length_of_long_occ:  #change in user defined variables
            long_occ_count = long_occ_count + 1
    resid_long_occupancy[n] = (resid, long_occ_count)  #same shape as resid_tmax but with the count of sig occupancies instead of max


np.save('%s/resid_tmax.%s.npy' %(outdir, lipid), resid_tmax)
np.save('%s/resid_long_occupancy.%s.npy' %(outdir, lipid), resid_long_occupancy)




####################################################################
############################### PLOTTING  ##########################
###################################################################

#prot.add_TopologyAttr(md.core.topologyattrs.Tempfactors(np.zeros(len(prot.atoms))))  #only pdb files have b factor, we have to add one and then write out pdb

#plt.bar(resid_tmax[:,0], resid_tmax[:,1])
#plt.xlabel('Residue number')
#plt.ylabel('# continuous ns with %s' %lipid)
#plt.xlim(0, len(resid_tmax))
#plt.savefig('res_vs_occupancy.%s.png' %lipid)


wid = 0.8
fig = plt.figure()

ax1 = fig.add_subplot(111)
line1 = ax1.bar(resid_tmax[:,0], resid_tmax[:,1], label = 'tmax', color = 'orange', width = wid)

ax2 = fig.add_subplot(111, sharex = ax1, frameon = False)
line2 = ax2.bar(resid_long_occupancy[:,0] + wid, resid_long_occupancy[:,1], label = 'long occ', color = 'green', width = wid)

ax2.yaxis.tick_right()
ax2.yaxis.set_label_position('right')
ax2.set_ylabel('# times longer than %s ns near %s' % (str(length_of_long_occ), lipid))
ax1.set_ylabel('Max continuous ns near %s' %lipid)
plt.xlabel('Residue number')

plt.xlim(0, len(resid_tmax))
plt.legend((line1, line2), ('Tmax', 'Counts'))
title = trajdir.split('/')[3] + ' ' + trajdir.split('/')[4]
plt.title(title)
plt.savefig('%s/res_vs_occupancy_vs_counts.%s.png' %(outdir, lipid), dpi = 800)



'''

#####################################################################################
#################### MAKING PDBS COLORED BY BETA ######################################
#################################################################################

resid_tmax[:,1] = resid_tmax[:,1]/100
### WRITE PDB for CG model
prot.write("GLUT5_prot.%s.pdb" %lipid)  #save protein only pdb
u = md.Universe('GLUT5_prot.%s.pdb' %lipid)   #open again to fix beta column
u.atoms.tempfactors = resid_tmax[:,1] # b is 10.0 max, so now 113 = 11.3 tex
u.atoms.write('GLUT5_prot_B.%s.pdb' %lipid)



#### ATOMISTIC MODEL
atomistic = md.Universe('/data2/GLUT5/4YBQ_complete.pdb')
atomistic.add_TopologyAttr('bfactors')
# have to do the assignment per atom, not per residue. Therefore loop through each residue, assign the tmax value for 
## as many atoms at the residue has (= length of list_atoms ). Append this to one large list, will be the same size as 
### atomistic.residues.atoms 

atoms_tmax = []
for n, list_atoms in enumerate(atomistic.residues.tempfactors):
    tmax_beta = resid_tmax[:,1][n]
    for index, val in enumerate(list_atoms):
        list_atoms[index] = tmax_beta
        atoms_tmax.append(list_atoms[index])


atomistic.residues.atoms.tempfactors = atoms_tmax
atomistic.atoms.write('GLUT5_atomistic_B.%s.pdb' %lipid)

### doing the same thing as above but to have Beta on trajectory
prot = system.select_atoms('name BB SC1 SC2 SC3 SC4')
prot.write('GLUT5_SYSTEM_B.%s.pdb' %lipid)
prot = md.Universe('GLUT5_SYSTEM_B.%s.pdb' %lipid)

atoms_tmax = []
for n, list_atoms in enumerate(prot.residues.tempfactors):
    tmax_beta = resid_tmax[:,1][n]
    for index, val in enumerate(list_atoms):
        list_atoms[index] = tmax_beta
        atoms_tmax.append(list_atoms[index])


prot.residues.atoms.tempfactors = atoms_tmax
prot.atoms.write('GLUT5_SYSTEM_B.%s.pdb' %lipid)
system.atoms.write('systemdelete.pdb')

print 'Cut the protein from systemdelete and << cat systemdelete.pdb >> GLUT5_SYSTEM_B.lipid.pdb  >> and delete the END in the middle'
print 'this gives you the CG protein in the system, with the beta so you can look at the beta coloring in the analysis'


'''
