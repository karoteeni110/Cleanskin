# !/bin/bash
dddd='1701'

if cd /home/yzan/Desktop/try/$dddd ; then
  pwd
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for gz in *$dddd* ; do
  basename=${gz%.*} # DONT USE ${gz:0:-3} !!!
  if tar -xzf $gz --one-top-level==$basename ; then 
    rm $gz
  elif mkdir ./=$basename ; mv $gz $_ ; then
    gunzip -rdN ./=$basename/$gz # retains the original filename
  else 
    mv $gz Acluster # just in case, expected to be empty
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter