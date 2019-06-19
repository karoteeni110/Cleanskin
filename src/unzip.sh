# !/bin/bash
dddd='0002'

if cd /home/yzan/Desktop/try; then
  pwd
else
  echo 'Could not change directory! Aborting.' 1>&2
  exit 1
fi

for basename in *$dddd* ; do # untar 
  if [ tar -xvzf $basename --one-top-level==$basename ]; 
  then 
      ; #do nothing
  elif [ tar -xvf $basename --one-top-level==$basename ]; 
  then 
      ; #do nothing
    else # pdf, html
      mv ./Acluster
  fi
done

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