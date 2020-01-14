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

def df2xy(df):
    catedict = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
    df.pid = df.pid.map(catedict)
    df = df.dropna(subset=['pid'])
    df.pid = df.pid.apply(lambda x: tuple(x))
    X = df.iloc[:,1:].to_numpy()
    mlb = MultiLabelBinarizer()
    return X, mlb.fit_transform(df.pid), mlb.classes_

def cls_with_ft(ft_comp_df):
    X, y, y_lbs = df2xy(ft_comp_df.iloc[:1000,:])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    classif = OneVsRestClassifier(SVC(kernel='linear')).fit(X_train, y_train)

    for cate in y_lbs:
        pred = classif.predict(X_test)
        cate_acc = accuracy_score(y_test, pred)
        print(cate, cate_acc)

if __name__ == "__main__":
    abst_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_abstract_comp.txt'
    ft_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_ft_comp.txt'

    abst_comp, ft_comp = read_data(abst_comp_path), read_data(ft_comp_path)
    cls_with_ft(ft_comp)
    print()
