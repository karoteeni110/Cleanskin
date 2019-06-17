# !/bin/bash

if cd ../data/0002; then
  gunzip *0002*.gz
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for basename in *0002* ; do # untar
  if [ ${basename: -4} != ".pdf" ] || [ $basename != cluster*]; then 
    tar -xvf "$basename" --one-top-level=="$basename" 
  fi
  if [[ ! $basename =~ "=" ]] ; then # if not a directory, move to /cluster
    mv $basename ./cluster/
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter