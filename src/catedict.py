from paths import cate_path
from os import listdir
from os.path import basename

def add2_dict(d, f):
    with open(f,'r') as txt:
        lines = txt.readlines()
    cate = basename(f)[-4]
    for line in lines:
        artID = line.split()[0]
        d[artID].append(cate)    