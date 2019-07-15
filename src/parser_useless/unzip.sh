# !/bin/bash

# Decompresses the tarballs in $dir, keeping the original structure
# PDFs are also kept in folder.
# Cannot extract withdrawn articles.
# To check the articles that don't show (usually caused by withdrawn articles), use src/checkdiff.py

dddd='1701'
dir='/home/yzan/Desktop/try/1701_002'

if cd $dir ; then
  pwd
fi
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for gz in *$dddd* ; do
  basename=${gz%.*} # DONT USE ${gz:0:-3} !!!
  if tar -xzf $gz --one-top-level==$basename ; then 
    rm $gz
  elif mkdir ./=${basename} ; mv ${gz} $_ ; then
    gunzip -rdN ./=${basename}/${gz} # retains the original filename
  else 
    mv $gz Acluster # just in case, expected to be empty
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter