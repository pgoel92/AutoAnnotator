#!/bin/bash

trfile='txt.tr'
cat ../etc/$2/$trfile | $CMULM/bin/text2wfreq > ../etc/$2/$trfile.wfreq 
cat ../etc/$2/$trfile.wfreq | $CMULM/bin/wfreq2vocab > ../etc/$2/$trfile.vocab
cat ../etc/$2/$trfile | $CMULM/bin/text2idngram -n 3 -vocab ../etc/$2/$trfile.vocab -idngram ../etc/$2/$trfile.idngram
$CMULM/bin/idngram2lm -n 3 -vocab ../etc/$2/$trfile.vocab -idngram ../etc/$2/$trfile.idngram -arpa ../etc/$2/$trfile.lm
$SPHINXDIR/bin/sphinx3_lm_convert -i ../etc/$2/$trfile.lm -o ../models/lm/$1.lm.dmp
rm ../etc/$2/$trfile.wfreq ../etc/$2/$trfile.vocab ../etc/$2/$trfile.idngram ../etc/$2/$trfile.lm
rm -rf cmuclm*
