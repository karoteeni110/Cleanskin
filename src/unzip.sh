# !/bin/bash
dddd='0002'

if cd /home/yzan/Desktop/try; then
  pwd
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for basename in *$dddd* ; do # untar 
  if tar -xzf $basename --one-top-level==${basename:0:-3} ; then 
      rm $basename 
  elif gunzip $basename ; then 
      mv ${basename:0:-3} ./Acluster # without '.gz'
  else # pdf, html
      mv $basename ./Acluster
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter