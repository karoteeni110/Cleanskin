# !/bin/bash
dddd='0001'

if cd /home/yzan/Desktop/try/$dddd ; then
  pwd
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for gz in *$dddd* ; do
  basename=${gz:0:-3}
  if tar -xzf $gz --one-top-level==$basename ; then 
      rm $gz
  elif gunzip -cd $gz > single.tex && rm $gz ; then 
      mkdir ./=$basename ; mv single.tex $_
  else # pdf, html
      mv $gz Acluster
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter