from paths import cate_path, results_path
from os import listdir
from os.path import basename, join
from collections import defaultdict
import pickle   

def get_dicts(txtpath):
    cate2artsdict, art2catedict = defaultdict(set), defaultdict(set)
    with open(txtpath, 'r') as f:
        for line in f.readlines():
            artid, catelist = line.split()[0], line.split()[1].split(',')
            art2catedict[artid].union(set(catelist))
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

def dump_dicts(cate2arts, art2cates):
    with open(join(results_path, 'cate2arts.pkl'), 'wb') as d1:
        pickle.dump(cate2arts, d1)
    print('cate2arts -- dumped.')
    with open(join(results_path, 'arts2cate.pkl'), 'wb') as d2:
        pickle.dump(art2cates, d2)
    print('art2cates -- dumped.')

if __name__ == "__main__":
    cate2arts, art2cates = defaultdict(set), defaultdict(set)
    for txt in listdir(cate_path):
        print('Collecting: %s' % txt)
        txtpath = join(cate_path, txt)
        c2a, a2c = get_dicts(txtpath)
        cate2arts, arts2cate = merge_dicts(cate2arts, c2a), merge_dicts(art2cates, a2c)
    # print(cate2arts['astro-ph'])
    
    dump_dicts(cate2arts, art2cates)
        


