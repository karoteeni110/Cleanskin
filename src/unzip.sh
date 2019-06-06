#!/bin/bash

#gunzip astro-*.gz

for basename in *0001* ; do # untar
  tar -xvf "$basename" --one-top-level=="$basename" 
  if [[ ! $basename =~ "=" ]] ; then # if it's not a directory, move to /cluster
    mv $basename cluster
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter