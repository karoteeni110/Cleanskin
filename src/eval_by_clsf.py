"""Evaluate topic models with multilabel classification"""
from kldiv import read_data, get_pid2cate_dict

from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import itertools


def example():
    X, Y = make_multilabel_classification(n_classes=2, n_labels=1,
                                      allow_unlabeled=True,
                                      random_state=1)
    classif = OneVsRestClassifier(SVC(kernel='linear'))
    pred = classif.fit(X, Y).predict(X)

def df2xy(train_df, test_df):
    """"""
    mlb = MultiLabelBinarizer()
    for xdf in [0,1]:
        df = [train_df, test_df][xdf]
        df.pid = df.pid.map(CATEDICT)
        df = df.dropna(subset=['pid']) # Drop those categories 
        df.loc[:,'pid'] = df.pid.apply(lambda x: tuple(x)) # list to tuple 
        if xdf == 0: # if it is train df
            X_train = df.iloc[:,1:].to_numpy()
            y_train = mlb.fit_transform(df.pid)
        else: # test df
            X_test = df.iloc[:,1:].to_numpy()
            y_test = mlb.transform(df.pid) # DIFFERENT FROM fit_transform!!!
    # return X, mlb.fit_transform(df.pid), mlb.classes_
    return X_train, X_test, y_train, y_test, mlb.classes_

def cls_with_ft(train_df, test_df):
    X_train, X_test, y_train, y_test, y_lbs = df2xy(train_df, test_df)
    classif = OneVsRestClassifier(SVC(kernel='linear')).fit(X_train, y_train)
    
    pred = classif.predict(X_test)
    y_test, pred = y_test.T, pred.T # transpose for cate-wise comparing 
    for idx, cate in enumerate(y_lbs):
        cate_acc = accuracy_score(y_test[idx], pred[idx])
        print(cate, cate_acc)

if __name__ == "__main__":
    abst_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_related_work_comp.txt'
    ft_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_ft_comp.txt'

    # abst_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs/cs_testcomp/cs_50_perdoc.txt'
    # ft_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs/model_50/composition.txt'

    abst_comp, ft_comp = read_data(abst_comp_path), read_data(ft_comp_path)
    CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
    cls_with_ft(train_df=abst_comp.sample(n=10000), test_df=ft_comp.sample(n=10000))
    print()
