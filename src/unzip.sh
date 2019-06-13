# !/bin/bash

gunzip 1701.*.gz

for basename in 1701.* ; do # untar
  if [ ${basename: -4} != ".pdf" ] || [ $basename = cluster*]; then 
    tar -xvf "$basename" --one-top-level=="$basename" 
  fi
  if [[ ! $basename =~ "=" ]] ; then # if not a directory, move to /cluster
    mv $basename cluster17
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter