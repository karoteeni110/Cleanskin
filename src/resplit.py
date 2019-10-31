from os import listdir
from os.path import join
from random import choice
from kldiv import get_pid2meta
from paths import metadatas_path, perpsets_traindir, perpsets_testdir
from shutil import move
import pandas as pd

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

if __name__ == "__main__":
    train_pid2cate = get_pid2dst(listdir(perpsets_traindir), ['Computer_Science.xml'])
    test_pid2cate = get_pid2dst(listdir(perpsets_traindir), ['Computer_Science.xml'])
    for cate in set(train_pid2cate):
        traincount = len(train_pid2cate[train_pid2cate==cate])
        test_in_cate = test_pid2cate[test_pid2cate==cate]
        testcount = len(test_in_cate)
        dif = testcount/(traincount+testcount)
        if dif > 0.1:
            test_shouldbe = int((traincount+testcount)*0.1)
            tomove = testcount-test_shouldbe
            print(cate, 'papers to move: %s' % tomove)
        #     for pid in test_in_cate[:tomove]:
        #         move(join(perpsets_testdir, pid+'.txt'), join(perpsets_traindir, pid+'.txt'))
        # print('Moved articles: %s' % tomove)
    
