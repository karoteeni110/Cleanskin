"""
Moves the "article folder" with multiple tex files to data/specialcase.

Usage:
    Get the folder list with noBib.py ('00error.txt');
    Enter the relpath of '00error.txt' in /results as sysarg[1], in the format of '1701/log/00error.txt'.
    e.g.: python3 specialcase_mover.py 1701/log/00error.txt
"""
import sys, shutil
from os.path import join
from os import listdir
from paths import results_path, data_path

fl_path = join(results_path, sys.argv[1])
with open(fl_path, 'r') as flfile:
    fl = flfile.readlines()
fl = [line.split()[-1] for line in fl if line.split()[-1][-4:].isdigit()] # Special case list: ['', '=1701.01118', ...]

fournum_dir = sys.argv[1][:4] # 1701
src = join(data_path, fournum_dir) # root/data/1701
list_dir = listdir(src) # ['=1701.00001', '=1701.00002', ...]
dest = join(data_path, 'special') # root/data/special

for sub_dir in list_dir:
    if sub_dir in fl:
        dir_to_move = join(src, sub_dir) # root/data/1701/=1701.01314
        shutil.move(dir_to_move, dest)