wdir=/data2/coarse_graining/POPC.POPE.POPS.POSM.POPA/IN
gro=4YB9.1.us.gro
xtc=4YB9.1-5.us.skip10.xtc

read -r -p "Make analysis directory in $wdir? [y/n] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
	mkdir $wdir/analysis 
	echo 'making analysis directory'
else
	echo 'skipping directory making' 
fi


echo 'POPS in ' $wdir ' with ' $gro ' ' $xtc
python tmax_calc.py POPS $wdir $gro $xtc

echo 'POPE in ' $wdir ' with ' $gro ' ' $xtc
python tmax_calc.py POPE $wdir $gro $xtc


echo 'POPA in ' $wdir ' with ' $gro ' ' $xtc
python tmax_calc.py POPA $wdir $gro $xtc


echo 'POSM in ' $wdir ' with ' $gro ' ' $xtc
python tmax_calc.py POSM $wdir $gro $xtc


echo 'POPC in ' $wdir ' with ' $gro ' ' $xtc
python tmax_calc.py POPC $wdir $gro $xtc
