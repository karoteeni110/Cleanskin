from kldiv import get_pid2meta
from paths import fulltext_dir, metadatas_path
from shutil import copy
from os import listdir
from random import choice, shuffle
from collections import Counter
import pandas as pd

def mk_cate_dirs(dst=''):
    return 0

def get_pid2dst(metaxml_list=listdir(metadatas_path)):
    pid2meta = get_pid2meta(metaxml_list)
    pid2cates = dict()
    cate2pcount = Counter()
    for pid in pid2meta:
        pcate = choice([c[3:] for c in pid2meta[pid]['categories'].split(', ') 
                            if c[:2]=='cs'])
        pid2cates[pid] = pcate
        cate2pcount[pcate] += 1
    print("Papers categorized. Summary:")
    for cate in cate2pcount:
        print(cate, ":", cate2pcount[cate])
    print()
    cate2pcount = pd.Series(cate2pcount)
    return pid2cates, cate2pcount

def copy_to_catedir(pid, cate):
    src = ''
    dst = ''
    copy(src, dst)
    


if __name__ == "__main__":
    catedir_paths = mk_cate_dirs()
    cs_paper_pids = [i[:-4] for i in listdir(fulltext_dir) if i[:-3]=='txt']
    pid2cate, cate2pcount = get_pid2dst()
    
    cs_paper_pids = shuffle(cs_paper_pids)
    for pid in cs_paper_pids:
        copy_to_catedir(pid, pid2cate[pid])