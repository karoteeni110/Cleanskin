from kldiv import get_pid2meta, get_acro2cate_dict
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
    print('Collecting categories...')
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

def copy_to_catedir(paperfn, cate):
    src = join(PAPERDIR, paperfn)
    to_trainset = cate2train_toadd[cate]
    if to_trainset:
        dst = join(perpsets_traindir, paperfn)
        cate2train_toadd[cate] -= 1
        if cate2train_toadd[cate] == 0:
            print(cate, 'training set collection done. %s/%s' % 
                        (len(cate2train_toadd[cate2train_toadd==0]), len(cate2train_toadd)))
        if cate2train_toadd[cate] % 100 == 0:
            print('Cate:', cate+'('+acro2cate[cate]+')', 'papers to add:', cate2train_toadd[cate])
    
    else:
        dst = join(perpsets_testdir, paperfn)
    copy(src, dst)
    


if __name__ == "__main__":
    catedir_paths = mk_cate_dirs()
    print('Listdir:', fulltext_dir, '...')
    cs_paper_fns = listdir(fulltext_dir) # [i[:-4] for i in listdir(fulltext_dir) if i[-3:]=='txt']
    shuffle(cs_paper_fns)
    print('... Listdir done.')
    pid2cate, cate2pcount = get_pid2dst(['Computer_Science.xml'])
    acro2cate = get_acro2cate_dict()

    cate2train_toadd = pd.Series(cate2pcount*0.9, dtype='int')
    PAPERDIR = fulltext_dir
    for paperfn in cs_paper_fns:
        pid = paperfn[:-4] # strip '.txt'
        copy_to_catedir(paperfn, pid2cate.pop(pid))