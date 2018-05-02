#####################################################################################
#################### MAKING PDBS COLORED BY BETA ######################################
#################################################################################
import numpy as np
import MDAnalysis as md 

trajdir = '/data2/coarse_graining/POPC.POPE.POPS.POSM.POPA.EQUAL/OUT/'
lipid = 'POPC'
pdb_f = '4YBQ'
atomistic = md.Universe('/data2/coarse_graining/4YBQ.pdb')
#atomistic = md.Universe('/data2/coarse_graining/homology_modeling/4YB9/4YB9.pdb')  ### OBS YOU CHANGED 4YB9 SO YOU NEED THE OLD ONE


############################################################

tmax = np.load(trajdir + 'analysis/' + 'resid_tmax.%s.npy' % lipid)
tmax[:,1] = tmax[:,1]/ 100 # need b to be on a scale of 100, doesn't really matter if /10 or /100 or /1000 just needs to be smaller than 100


print 'ATOMISTIC PROTEIN'

# have to do the assignment per atom, not per residue. Therefore loop through each residue, assign the tmax value for 
## as many atoms at the residue has (= length of list_atoms ). Append this to one large list, will be the same size as 
### atomistic.residues.atom

atoms_tmax = []
for n, list_atoms in enumerate(atomistic.residues.tempfactors):  #don't need these, we will reassign, we are looping through these to rename them 
	tmax_beta = tmax[:,1][n]
	for index, val in enumerate(list_atoms):
		list_atoms[index] = tmax_beta    #basically just giving the whole row the correct tmax, will match for each row of atoms per residue (since tmax only has info per residue)
		atoms_tmax.append(list_atoms[index])  #make a big list with these new reassigned values, then we have a list of matching length to atomistic.residues.tempfactors, so you can just replace

atomistic.residues.atoms.tempfactors = atoms_tmax
atomistic.atoms.write(trajdir + 'analysis/' + pdb_f + '.' + lipid + '.atomistic.pdb')

print 'COARSE GRAINED PROTEIN'
cg = md.Universe(trajdir + 'production/' + pdb_f + '.1.us.gro')
cg = cg.select_atoms('name BB')
cg.write(trajdir + 'analysis/DELETEPDB.pdb')  #need to write a pdb because gro doesnt have tempfactors
cg = md.Universe(trajdir + 'analysis/DELETEPDB.pdb')
cg.atoms.tempfactors = tmax[:,1]
cg.atoms.write(trajdir + 'analysis/' + pdb_f + '.' + lipid + '.CG.pdb')





'''
IF YOU WANT IT TO BE IN THE TRAJ, SEE BELOW!!!


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