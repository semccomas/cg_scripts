#!/bin/bash

# Submit to the tcb partition
#SBATCH -p tcb

# The name of the job in the queue
#SBATCH -J eq_OUT
# wall-clock time given to this job
#SBATCH -t 00:30:00

# Number of nodes and number of MPI processes per node
#SBATCH -N 1 --ntasks-per-node=10


# Output file names for stdout and stderr
#SBATCH -e error.err -o output.out

module load gromacs/2016.1
prot=4YBQ

topoldir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS/OUT/4YBQ_charmm
outdir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS/OUT/equilibration
mdpdir=/nethome/mccomas/coarse_graining/STRICT_EQUILIBS  #use this if you need strict equilibrations

#minimization
gmx grompp -f $mdpdir/step6.0_equilibration.mdp -o $outdir/minim.tpr -c $topoldir/step5_assembly.box.pdb -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/minim -cpi $outdir/minim.cpt

gmx grompp -f $mdpdir/step6.1_equilibration.mdp -o $outdir/$prot.1.eq.tpr -c $outdir/minim.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.1.eq -cpi $outdir/$prot.1.eq.cpt

gmx grompp -f $mdpdir/step6.2_equilibration.mdp -o $outdir/$prot.2.eq.tpr -c $outdir/$prot.1.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.2.eq -cpi $outdir/$prot.2.eq.cp

gmx grompp -f $mdpdir/step6.3_equilibration.mdp -o $outdir/$prot.3.eq.tpr -c $outdir/$prot.2.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.3.eq -cpi $outdir/$prot.3.eq.cp -rdd 1.4

gmx grompp -f $mdpdir/step6.4_equilibration.mdp -o $outdir/$prot.4.eq.tpr -c $outdir/$prot.3.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.4.eq -cpi $outdir/$prot.4.eq.cp -rdd 1.4

gmx grompp -f $mdpdir/step6.5_equilibration.mdp -o $outdir/$prot.5.eq.tpr -c $outdir/$prot.4.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.5.eq -cpi $outdir/$prot.5.eq.cp -rdd 1.4

gmx grompp -f $mdpdir/step6.6_equilibration.mdp -o $outdir/$prot.6.eq.tpr -c $outdir/$prot.5.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.6.eq -cpi $outdir/$prot.6.eq.cp -rdd 1.4

gmx grompp -f $mdpdir/step6.7_equilibration.mdp -o $outdir/$prot.7.eq.tpr -c $outdir/$prot.6.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.7.eq -cpi $outdir/$prot.7.eq.cp #-rdd 1.4

gmx grompp -f $mdpdir/step6.8_equilibration.mdp -o $outdir/$prot.8.eq.tpr -c $outdir/$prot.7.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/$prot.8.eq -cpi $outdir/$prot.8.eq.cp #-rdd 1.4
