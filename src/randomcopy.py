from random import choice
from shutil import copy
from paths import results_path, cleanedxml_path
from os import listdir
from os.path import join

def copyten():
    for _ in range(0,10):
        fn = choice(listdir(cleanedxml_path))
        src = join(cleanedxml_path, fn)
        dst = join(results_path, fn)
        copy(src, dst)


if __name__ == "__main__":    
    copyten()