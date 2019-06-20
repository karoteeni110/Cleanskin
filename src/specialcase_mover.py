"""
Moves the "article folder" with multiple tex files to data/specialcase.

Usage:
    Get the folder list ('00error.txt') from regexCleaner.py;
    Enter dddd as the arg.
    e.g.: python3 specialcase_mover.py 1701        /log/00error.txt
"""
import sys
from shutil import copytree
from os.path import join, dirname, basename, relpath
from os import listdir
from paths import results_path, data_path

dddd = sys.argv[1]

fl_path = join(results_path, '%s/log/00error.txt' % sys.argv[1])
with open(fl_path, 'r') as flfile:
    fl = flfile.readlines()
pathlist = [line.strip('Overwriting err at:') for line in fl] # '.../data/0001/=hep-ph0001171/mu2.tex'

def get_artIDdir_in_data(path):
    relp = relpath(path, data_path + '/%s' % dddd) # '=hep-ph0001171/mu2.tex'
    artIDdir = relp.split('/')[0] # ['=hep-ph0001171/', 'mu2.tex']
    return artIDdir

dirlist = [get_artIDdir(p) for p in pathlist]
dirlist = set(dirlist)

for dir_to_cp in dirlist:
    dest = join(data_path, 'moreThan1Tex/%s' % basename(dir_to_cp) ) # '.../data/moreThan1Tex/=hep-ph0001171'
    copytree(dir_to_cp, dest)