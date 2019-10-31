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

def get_pid2dst(allpids, metaxml_list=listdir(metadatas_path)):
    """Returns: pid2cates -- dictionary 
                            key: pid
                            value: CS subcategory acronym
                cate2pcount -- pd series
                            index: CS subcate acronym
                            value: count of papers in the subcate
    """
    pid2cate = pd.Series(get_pid2meta(metaxml_list)) # strip '.txt'

    print('Collecting categories...')
    pid2cate = pid2cate.apply(lambda x: x.get('categories').split(', '))
    pid2cate = pid2cate.apply(lambda cates: [c[3:] for c in cates if c[:2]=='cs'] )
    pid2cate = pid2cate.apply(lambda subcates: choice(subcates))
    pid2cate = pid2cate[pid2cate.index.isin(allpids)]

    cate2pcount = dict()
    for subcate in set(pid2cate):
        cate2pcount[subcate] = len(pid2cate[pid2cate==subcate])
    print("Papers categorized. Summary:")
    for cate in cate2pcount:
        print(cate, ":", cate2pcount[cate])
    print()

    cate2pcount = pd.Series(cate2pcount)
    return pid2cate, cate2pcount
    return 0


def copy_to_catedir(paperfn, cate, test_to_add):
    src = join(PAPERDIR, paperfn)
    if test_to_add > 0:
        dst = join(perpsets_testdir, paperfn)
        gototest = 1
    else:
        dst = join(perpsets_traindir, paperfn)
        gototest = 0
    copy(src, dst)
    return gototest

if __name__ == "__main__":
    # catedir_paths = mk_cate_dirs()
    print('Listdir:', fulltext_dir, '...')
    cs_paper_fns = listdir(fulltext_dir) # [i[:-4] for i in listdir(fulltext_dir) if i[-3:]=='txt']
    shuffle(cs_paper_fns)
    allpids = pd.Series(cs_paper_fns)
    allpids = allpids.apply(lambda x:x[:-4])
    print('... Listdir done.')
    
    pid2cate, cate2pcount = get_pid2dst(allpids, ['Computer_Science.xml'])
    # acro2cate = get_acro2cate_dict()

    # totest, totrain = pd.Series(), pd.Series()
    # for cate in set(pid2cate):
    #     papers_in_cate = pid2cate[pid2cate==cate]
    #     sumcount = len(papers_in_cate)
    #     boundary = int(sumcount*0.1)
    #     totest = totest.append(papers_in_cate[:boundary].index.to_series())
    #     totrain = totrain.append(papers_in_cate[boundary:].index.to_series())

    cate2test_toadd = pd.Series(cate2pcount*0.1, dtype='int')
    sumkeeper = cate2test_toadd.copy()
    PAPERDIR =  fulltext_dir # join(results_path, 'test')
    for paperfn in cs_paper_fns:
        pid = paperfn[:-4] # strip '.txt'
        try:
            cate = pid2cate.pop(pid)
            
            gototest = copy_to_catedir(paperfn, cate, cate2test_toadd.at[cate])
            if gototest:
                cate2test_toadd[cate] -=1

            # if old.equals(cate2test_toadd):
            #     print('counter does not change')
            #     exit(0)

            done = sumkeeper.at[cate]-cate2test_toadd.at[cate]
            if done % 50 == 0:
                print('Test set for', cate+':', 
                        done, '/', sumkeeper.at[cate], str(done*100/sumkeeper.at[cate])+'%%')

        except KeyError:
            continue