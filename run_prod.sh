#!/bin/bash

# Submit to the tcb partition
#SBATCH -p tcb

# The name of the job in the queue
#SBATCH -J equal_out
# wall-clock time given to this job
#SBATCH -t 24:00:00

# Number of nodes and number of MPI processes per node
#SBATCH -N 1 --ntasks-per-node=24


# Output file names for stdout and stderr
#SBATCH -e error.err -o output.out

module load gromacs/2016.1
cnt=1
cntmax=15
prot=4YBQ

topoldir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS.POSM.POPA.EQUAL/OUT/4YBQ_charmm
outdir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS.POSM.POPA.EQUAL/OUT/production
eqdir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS.POSM.POPA.EQUAL/OUT/equilibration
proddir=/nethome/mccomas/coarse_graining


while [ "$cnt" -le "$cntmax" ]
do
        pcnt=$((cnt-1))
        if [ "$cnt" -eq 1 ] ## need special params for 1
        then
                if [ -f $eqdir/$prot.9.eq.gro ]; then #don't need this we know it exists but makes the script symmetrical :) 
                        if [ ! -f $outdir/$prot.$cnt.us.tpr ]; then #if you haven't already made TPR then do it
                                gmx grompp -f $proddir/production.mdp -o $outdir/$prot.$cnt.us.tpr -c $eqdir/$prot.9.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
                        fi
                        if [ ! -f $outdir/$prot.$cnt.us.gro ]; then #if you haven't already run this sim, then do it
                                gmx mdrun -deffnm $outdir/$prot.$cnt.us -cpi $outdir/$prot.$cnt.us.cpt
                        fi
                fi



        else
                if [ -f $outdir/$prot.$pcnt.us.gro ]; then   #if you have finished the last run, then move on
                        if [ ! -f $outdir/$prot.$cnt.us.tpr ]; then #if you haven't already made TPR then do it
                                gmx grompp -f $proddir/production.mdp -o $outdir/$prot.$cnt.us.tpr -c $outdir/$prot.$pcnt.us.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
                        fi
                        if [ ! -f $outdir/$prot.$cnt.us.gro ]; then #if you haven't already run this sim, then do it
                                gmx mdrun -deffnm $outdir/$prot.$cnt.us -cpi $outdir/$prot.$cnt.us.cpt
                        fi
                fi
        fi

        cnt=$((cnt+1))
done
~                                                                                                                                        
~                   
