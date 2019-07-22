from paths import cate_path
from os import listdir
from os.path import basename, join
from collections import defaultdict
import pickle   


art2cate = {}
cate2arts = {}

def get_dicts(txtpath):
    cate2artsdict, art2catedict = defaultdict(set), defaultdict(set)
    with open(txtpath, 'r') as f:
        for line in f.readline():
            artid, catelist = line.split()[0], line.split()[1].split(',')
            art2catedict[artid].add(set(catelist))
            for cate in catelist:
                cate2artsdict[cate].add(artid)
    return cate2artsdict, art2catedict

def merge_dicts(dict1, dict2):
    for k in dict2:
        if k in dict1:
            dict1[k] = dict1[k].union(dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1

for txt in listdir(cate_path):
    txtpath = join(cate_path, txt)
    c2a, a2c = get_dicts(txtpath)


