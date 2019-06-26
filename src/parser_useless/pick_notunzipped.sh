# !/bin/bash

dddd='1701'

# ========================

if cd /home/yzan/Desktop/arXiv/$dddd ; then
  pwd
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi
# CHANGE FnArray for every dddd
declare -a FnArray=('1701.01247' '1701.01292' '1701.01020')

for fn in "${FnArray[@]}"; do
    cp -i $fn.gz ../../try/${dddd}short/ # be warned before overwriting
done

# ========================

if cd /home/local/yzan/Desktop/try/${dddd}short; then
    for i in *.gz; do mkdir =${i:0:-3}; done
    for i in *.gz; do mv $i ${i:0:-3}; cd $_ ; gunzip -rdN $i; cd ..; done
fi
