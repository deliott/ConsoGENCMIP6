#!/bin/bash

cd /ccc/cont003/home/gencmip6/oboucher/CONSO/IRENE

rm -f toto toto2
ccc_myproject > toto
sed -n '/Irene Skylake/,${p}' toto | awk '/Irene Xlarge/ {exit} {print}' > toto2

#--DATE 
yr=$(date +"%Y")
da=$(date +"%j")
date=`python -c "print ${yr}.+${da}./366."`

#--CONSO TOTALE
conso=`grep Total toto2 | awk '{print $2}' | head -n 1`
echo "date conso totale=" $date $conso
echo $date $conso >> ./conso_totcmip6.dat

#--CONSO PAR MIP 
#for i in {1..25}
for i in {1..26}
do
mip=`grep p86ipsl toto2 | awk '{print $2}' | head -n ${i} | tail -n 1`
conso=`grep Subtotal toto2 | awk '{print $2}' | head -n ${i} | tail -n 1`
echo "date mip conso=" $date $mip $conso
echo $date $conso >> ./conso_${mip}.dat
done

rm -f toto toto2
