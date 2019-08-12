from random import choice
from shutil import copy
from paths import results_path, cleanedxml_path
from os import listdir
from os.path import join
import sys

def copyten(cp=10):
    for _ in range(0,cp):
        fn = choice(listdir(cleanedxml_path))
        src = join(cleanedxml_path, fn)
        dst = join(results_path, 'random_pick/' + fn)
        copy(src, dst)


if __name__ == "__main__":    
    copyten(int(sys.argv[1]))