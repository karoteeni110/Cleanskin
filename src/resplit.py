"""Correct the wrong split of train&test set for MALLET"""
from os import listdir
from os.path import join
from random import choice
from kldiv import get_pid2meta
from paths import metadatas_path, results_path
from shutil import move
import pandas as pd

def get_pid2dst(allpids, metaxml_list=listdir(metadatas_path)):
    """Returns: 
    pid2cates -- dictionary 
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
    train_pid2cate = pid2cate[pid2cate.index.isin(allpids[0])]
    test_pid2cate = pid2cate[pid2cate.index.isin(allpids[1])]

    traincount = dict()
    for subcate in set(train_pid2cate):
        traincount[subcate] = len(train_pid2cate[train_pid2cate==subcate])
    print("Train folder categorized. Summary:")
    for cate in traincount:
        print(cate, ":", traincount[cate])
    print()

    testcount = dict()
    for subcate in set(test_pid2cate):
        testcount[subcate] = len(test_pid2cate[test_pid2cate==subcate])
    print("Papers categorized. Summary:")
    for cate in testcount:
        print(cate, ":", testcount[cate])
    print()

    traincount = pd.Series(traincount)
    testcount = pd.Series(testcount)
    return train_pid2cate, traincount, test_pid2cate, testcount

if __name__ == "__main__":
    perpsets_traindir = '/home/ad/home/y/yzan/Desktop/Cleanskin/results/cs_lbsec/fulltext'
    perpsets_testdir = '/home/ad/home/y/yzan/Desktop/Cleanskin/results/cs_lbsec/cs_ft_test'

    print('Listdir: train')
    trainpids = pd.Series(listdir(perpsets_traindir)).apply(lambda x:x[:-4])
    print('... done')
    print('Listdir: test')
    testpids = pd.Series(listdir(perpsets_testdir)).apply(lambda x:x[:-4])
    print('... done')
    train_pid2cate, traincount, test_pid2cate, testcount = get_pid2dst([trainpids, testpids], ['Computer_Science.xml'])
    # , testcount = get_pid2dst(, ['Computer_Science.xml'])
    for cate in set(train_pid2cate):
        pid_in_train, pid_in_test = train_pid2cate[train_pid2cate==cate], test_pid2cate[test_pid2cate==cate]
        traincount, testcount = len(pid_in_train), len(pid_in_test)
        test_shouldbe = int((traincount+testcount)*0.1)
        tomove = testcount-test_shouldbe
        if tomove > 0:
            print(cate, 'papers to move: %s' % tomove)
            print()
            for x, pid in enumerate(pid_in_test.index[:tomove]):
                move(join(perpsets_testdir, pid+'.txt'), join(perpsets_traindir, pid+'.txt'))
                if (x+1)%30==0 or x+1==tomove:
                    print(cate, 'moved:', x)
        else:
            print(cate, 'papers to move: %s' % tomove)
            print()
            for x, pid in enumerate(pid_in_train.index[:(-tomove)]):
                move(join(perpsets_traindir, pid+'.txt'), join(perpsets_testdir, pid+'.txt'))
                if (x+1)%30==0 or x+1==tomove:
                    print(cate, 'moved:', x)
        print()