# !/bin/bash

dddd='0001'




if cd /home/yzan/Desktop/arXiv/$dddd ; then
  pwd
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

declare -a FnArray=('math0001067' 'quant-ph0001019' 'hep-th0001079' \
'math0001054' 'math0001180' 'astro-ph0001036' 'quant-ph0001115' 'math0001030')

for fn in "${FnArray[@]}"; do
    cp -i $fn.gz ../../try/${dddd}shorted/ # be warned before overwriting
done



# ========================

# if cd /home/local/yzan/Desktop/try/${dddd}shorted; then
#     for i in *.gz; do mkdir ${i:0:-3}; done
#     for i in *.gz; do mv $i ${i:0:-3}; cd $_ ; gunzip -rdN $i; cd ..; done
# fi
