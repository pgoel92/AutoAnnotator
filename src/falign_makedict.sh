#!/bin/bash
curdir=`pwd`
mkdir -p ../etc/$1/dicts
insentlist=`ls ../etc/$1/fdict_insent`
for file in $insentlist
do
	ind=${file#insent_}
	perl $TOOLS/MakeDict/make_pronunciation.pl -tools $TOOLS -dictdir $curdir/../etc/$1/ -words fdict_insent/insent_$ind -dict dicts/dict_$ind
done
rm -f logios.log
