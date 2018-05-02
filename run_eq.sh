#!/bin/bash

# Submit to the tcb partition
#SBATCH -p tcb

# The name of the job in the queue
#SBATCH -J PC_PE_PS_OUT
# wall-clock time given to this job
#SBATCH -t 4:00:00

# Number of nodes and number of MPI processes per node
#SBATCH -N 1 --ntasks-per-node=24


# Output file names for stdout and stderr
#SBATCH -e error.err -o output.out

module load gromacs/2016.1
cnt=1
cntmax=6
prot=4YBQ

topoldir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS/OUT/4YBQ_charmm
outdir=/nethome/mccomas/coarse_graining/POPC.POPE.POPS/OUT/equilibration

## minimization first
gmx grompp -f $topoldir/step6.0_equilibration.mdp -o $outdir/minim.tpr -c $topoldir/step5_assembly.box.pdb -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
gmx mdrun -deffnm $outdir/minim -cpi $outdir/minim.cpt


while [ "$cnt" -le "$cntmax" ]
do
        pcnt=$((cnt-1))
        if [ "$cnt" -eq 1 ] ## need special params for 1
        then
                if [ -f $outdir/minim.gro ]; then
                        if [ ! -f $outdir/$prot.$cnt.eq.tpr ]; then #if you haven't already made TPR then do it
                                gmx grompp -f $topoldir/step6.1_equilibration.mdp -o $outdir/$prot.$cnt.eq.tpr -c $outdir/minim.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
                        fi
                        if [ ! -f $outdir/$prot.$cnt.eq.gro ]; then #if you haven't already run this sim, then do it
                                gmx mdrun -deffnm $outdir/$prot.$cnt.eq -cpi $outdir/$prot.$cnt.eq.cpt
                        fi
                fi



        else
                if [ -f $outdir/$prot.$pcnt.eq.gro ]; then   #if you have finished the last run, then move on
                        if [ ! -f $outdir/$prot.$cnt.eq.tpr ]; then #if you haven't already made TPR then do it
                                gmx grompp -f $topoldir/step6.$((cnt))_equilibration.mdp -o $outdir/$prot.$cnt.eq.tpr -c $outdir/$prot.$pcnt.eq.gro -n $topoldir/index.ndx -p $topoldir/system.top -maxwarn 2
                        fi
                        if [ ! -f $outdir/$prot.$cnt.eq.gro ]; then #if you haven't already run this sim, then do it
                                gmx mdrun -deffnm $outdir/$prot.$cnt.eq -cpi $outdir/$prot.$cnt.eq.cpt
                        fi
                fi
        fi

        cnt=$((cnt+1))
done
~                                                                                                                                        
~                   
