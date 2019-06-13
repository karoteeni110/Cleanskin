# !/bin/bash
# 
# gunzip astro-*.gz

for basename in 1701.*. ; do # untar
  if [ ${basename: -4} != ".pdf" ]; then 
    tar -xvf "$basename" --one-top-level=="$basename" 
  if [[ ! $basename =~ "=" ]] ; then # if it's not a directory, move to /cluster
    mv $basename cluster
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter