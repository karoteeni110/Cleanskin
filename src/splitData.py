from kldiv import get_pid2meta, get_acro2cate_dict
from paths import fulltext_dir, metadatas_path, perpsets_testdir, perpsets_traindir, results_path
from shutil import copy
from os import listdir
from random import choice, shuffle
from collections import Counter
from os.path import join 
import pandas as pd
import numpy as np

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
    pid2cate= pd.Series(get_pid2meta(metaxml_list))
    pid2cate = pid2cate.apply(lambda x: x.get('categories').split(', '))
    pid2cate = pid2cate.apply(lambda cates: [c[3:] for c in cates if c[:2]=='cs'] )
    pid2cate = pid2cate.apply(lambda subcates: choice(subcates))

    print('Collecting categories...')
    cate2pcount = dict()
    for subcate in set(pid2cate):
        cate2pcount[subcate] = len(pid2cate[pid2cate==subcate])
    print("Papers categorized. Summary:")
    for cate in cate2pcount:
        print(cate, ":", cate2pcount[cate])
    print()

    cate2pcount = pd.Series(cate2pcount)
    return pid2cates, cate2pcount

def copy_to_catedir(paperfn, cate, cate2train_toadd):
    src = join(PAPERDIR, paperfn)
    to_testset = cate2test_toadd[cate]
    if to_testset>0:
        dst = join(perpsets_testdir, paperfn)
        cate2train_toadd[cate] -= 1
        if cate2train_toadd[cate] == 0:
            print(cate, 'training set collection done. %s/%s' % 
                        (len(cate2train_toadd[cate2train_toadd==0]), len(cate2train_toadd)))
        if (100-(cate2train_toadd[cate]/int(cate2pcount[cate]*0.9))*100)%5 ==0 : # Report every 5 percent
            print('Cate:', cate+'('+acro2cate[cate]+')', 'papers to add:', cate2train_toadd[cate])
    
    else:
        dst = join(perpsets_traindir, paperfn)
    copy(src, dst)
    


if __name__ == "__main__":
    catedir_paths = mk_cate_dirs()
    print('Listdir:', fulltext_dir, '...')
    cs_paper_fns = listdir(fulltext_dir) # [i[:-4] for i in listdir(fulltext_dir) if i[-3:]=='txt']
    shuffle(cs_paper_fns)
    print('... Listdir done.')
    pid2cate, cate2pcount = get_pid2dst(['Computer_Science.xml'])
    acro2cate = get_acro2cate_dict()

    cate2test_toadd = pd.Series(np.ones(len(cate2pcount))*3, index=cate2pcount.index) # pd.Series(cate2pcount*0.1, dtype='int')
    PAPERDIR = join(results_path, 'test') # fulltext_dir
    for paperfn in cs_paper_fns:
        pid = paperfn[:-4] # strip '.txt'
        try:
            cate = pid2cate.pop(pid)
            print('OLD:', cate, cate2test_toadd[cate])
            copy_to_catedir(paperfn, cate, cate2test_toadd)
            print('NEW:', cate, cate2test_toadd[cate])
        except KeyError:
            continue