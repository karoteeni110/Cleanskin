from random import choice
from shutil import copy
from paths import results_path, cleanedxml_path, cleaned_tmp0001_dir
from os import listdir
from os.path import join
import sys

def copyten(cp=10):
    source_dir = cleaned_tmp0001_dir
    for _ in range(0,cp):
        fn = choice(listdir(source_dir))
        src = join(source_dir, fn)
        dst = join(results_path, 'random_pick/' + fn)
        copy(src, dst)


if __name__ == "__main__":   
    if sys.argv[1]: 
        copyten(int(sys.argv[1]))
    else:
        copyten()