from kldiv import get_pid2meta
from paths import fulltext_dir, metadatas_path, perpsets_testdir, perpsets_traindir
from shutil import copy
from os import listdir
from random import choice, shuffle
from collections import Counter
from os.path import join 
import pandas as pd

def mk_cate_dirs(dst=''):
    return 0

def get_pid2dst(metaxml_list=listdir(metadatas_path)):
    """Returns: pid2cates -- dictionary 
                            key: pid
                            value: CS subcategory acronym
                cate2pcount -- pd series
                            index: CS subcate acronym
                            value: count of papers in the subcate
    """
    pid2meta = get_pid2meta(metaxml_list)
    pid2cates = dict()
    cate2pcount = Counter()
    print('Collecting paper categories...')
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

def copy_to_catedir(paperfn, cate, to_trainset):
    src = join(PAPERDIR, paperfn)
    if to_trainset:
        dst = join(perpsets_traindir, paperfn)
    else:
        dst = join(perpsets_testdir, paperfn)
    # copy(src, dst)
    


if __name__ == "__main__":
    catedir_paths = mk_cate_dirs()
    cs_paper_fns = listdir(fulltext_dir) # [i[:-4] for i in listdir(fulltext_dir) if i[-3:]=='txt']
    pid2cate, cate2pcount = get_pid2dst(['Computer_Science.xml'])
    
    cs_paper_fns = shuffle(cs_paper_fns)
    PAPERDIR = fulltext_dir
    for paperfn in cs_paper_fns:
        pid = paperfn[:-4] # strip '.txt'
        copy_to_catedir(paperfn, pid2cate[pid])