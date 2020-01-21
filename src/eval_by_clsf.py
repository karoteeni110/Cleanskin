"""Evaluate topic models with multilabel classification"""
from kldiv import read_data, get_pid2cate_dict, align_dfs

from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import pandas as pd
import itertools


def example():
    X, Y = make_multilabel_classification(n_classes=2, n_labels=1,
                                      allow_unlabeled=True,
                                      random_state=1)
    classif = OneVsOneClassifier(SVC(kernel='linear'))
    pred = classif.fit(X, Y).predict(X)

def df2train(df):
    """"""
    mlb, le = MultiLabelBinarizer(), LabelEncoder()    
    df.loc[:,'pid'] = df.pid.map(CATEDICT)
    df = df.dropna(subset=['pid']).sample(frac=1) # Drop those categories and shuffle
    df.loc[:,'pid'] = df.pid.apply(tuple)
    df.loc[:,'pid'] = df.pid.apply(sorted).apply(lambda x: ','.join(str(i) for i in x)) # list to str 
    X_train = df.iloc[:,1:].to_numpy()
        # y_train = mlb.fit_transform(df.pid) # [0,0,0,...,1] format labels
        # y_train = np.apply_along_axis(lambda bilb:','.join(str(i) for i in bilb), 1, y_train) # '010101' format labels
    y_train = le.fit_transform(df.pid)
        # X_test = df.iloc[:,1:].to_numpy()
        # # y_test = mlb.transform(df.pid) # DIFFERENT FROM fit_transform!!!
        # # y_test = np.apply_along_axis(lambda bilb:''.join(str(i) for i in bilb))
        # y_test = le.transform(df.pid)
    return X_train, y_train, le

def dfpid2cate(df):
    df.loc[:,'pid'] = df.pid.map(CATEDICT)
    df = df.dropna(subset=['pid']).sample(frac=1)
    df.loc[:,'pid'] = df.pid.apply(tuple)
    df.loc[:,'pid'] = df.pid.apply(sorted).apply(lambda x: ','.join(str(i) for i in x))
    return df

def df2test(df, cate, labeler, y_train):
    catedf = df.loc[df.pid.str.contains(cate)].loc[df.pid.isin(labeler.inverse_transform(y_train))]
    X_test = catedf.iloc[:,1:].to_numpy()
    y_test = labeler.transform(catedf.pid)
    return X_test, y_test

def cls_with_ft(train_df, test_df):
    X_train, y_train, le = df2train(train_df)
    print('Training...')
    classif = OneVsOneClassifier(SVC(kernel='linear')).fit(X_train, y_train)
    
    print('Testing...')
    print()
    # GET subfield wise test sets
    subfields = set([i for l in CATEDICT.values() for i in l])
    test_df = dfpid2cate(test_df)
    print('subfield, # of test samples, accuracy')
    for sf in subfields:
        X_test, y_test = df2test(test_df, sf, le, y_train)
        if len(X_test) == 0:
            continue
        print(sf, len(X_test), classif.score(X_test, y_test))

if __name__ == "__main__":
    abst_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_abstract_comp.txt'
    ft_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_ft_comp.txt'

    # abst_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs/cs_testcomp/cs_50_perdoc.txt'
    # ft_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs/model_50/composition.txt'

    abst_comp, ft_comp = read_data(abst_comp_path), read_data(ft_comp_path)
    CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
    # a = df2test(abst_comp, 'AI')
    # print()
    cls_with_ft(train_df=ft_comp.sample(frac=0.01), test_df=abst_comp.sample(frac=0.01))
    print()

    # TODO
    # a lot of the test data
    # ABSOLUTE NUMBER OF PAPER 