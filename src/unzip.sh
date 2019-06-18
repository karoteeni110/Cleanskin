# !/bin/bash
dddd='0002'

if cd /home/yzan/Desktop/try; then
  pwd
  gunzip ./*$dddd*.gz
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for basename in *$dddd* ; do # untar 
  if tar -xvzf $basename --one-top-level==$basename; then
    #pass
  else #if tar: This does not look like a tar archive
# tar: Skipping to next header
# tar: Exiting with failure status due to previous errors
    tar -xvf $basename --one-top-level==$basename

  else # pdf, html
    mv 
  fi



  if [ ${basename: -4} != ".pdf" ] ; then 
    tar -xvf "$basename" --one-top-level==$basename
  fi
  if [[ ! $basename =~ "=" ]] ; then # if not a directory, move to /cluster
    mv $basename ./Acluster/
  fi
done

# word="tiger"
# firstletter=${word:0:1}
# echo $firstletter