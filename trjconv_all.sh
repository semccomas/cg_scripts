start=1
stop=4
catout=1-5

working_dir=/data2/coarse_graining/POPC.POPE.POPS/OUT/production
intraj=4YBQ   #don't add xtc so we can add skip50 info


cd $working_dir
echo 0 > out.txt
while [ "$start" -le "$stop" ]
do
	gmx trjconv -f $intraj.$start.us.xtc -o $intraj.$start.us.skip10.xtc -s $intraj.$start.us.tpr -skip 10 -pbc whole < out.txt 

	start=$((start+1))

done

echo '"gmx trjcat -f `ls POPC.POPE.POPS/IN/production/4YB9.!(*-*).skip10.xtc | sort -t . -k 2n` -cat -nooverwrite -o $intraj.$catout.all.xtc"'

## yeah the above won't work in the script, just  paste into terminal and it will go
echo $intraj.$catout.all.xtc
echo 'use this for the -o flag gmx trjcat'
