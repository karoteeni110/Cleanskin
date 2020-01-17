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

def df2xy(train_df, test_df):
    """"""
    mlb, le = MultiLabelBinarizer(), LabelEncoder()
    train_df, test_df = align_dfs(train_df, test_df)
    for xdf in [0,1]:
        df = [train_df, test_df][xdf]
        df.pid = df.pid.map(CATEDICT)
        df = df.dropna(subset=['pid']).sample(frac=1) # Drop those categories and shuffle
        df.loc[:,'pid'] = df.pid.apply(tuple)
        df.loc[:,'pid'] = df.pid.apply(sorted).apply(lambda x: ','.join(str(i) for i in x)) # list to str 
        if xdf == 0: # if it is train df
            X_train = df.iloc[:,1:].to_numpy()
            # y_train = mlb.fit_transform(df.pid) # [0,0,0,...,1] format labels
            # y_train = np.apply_along_axis(lambda bilb:','.join(str(i) for i in bilb), 1, y_train) # '010101' format labels
            y_train = le.fit_transform(df.pid) 
        else: # test df
            X_test = df.iloc[:,1:].to_numpy()
            # y_test = mlb.transform(df.pid) # DIFFERENT FROM fit_transform!!!
            # y_test = np.apply_along_axis(lambda bilb:''.join(str(i) for i in bilb))
            y_test = le.transform(df.pid)
    return X_train, X_test, y_train, y_test, le.classes_

def cls_with_ft(train_df, test_df):
    X_train, X_test, y_train, y_test, y_lbs = df2xy(train_df, test_df)
    print('Training...')
    classif = OneVsOneClassifier(SVC(kernel='linear')).fit(X_train, y_train)
    
    print('Testing...')
    # GET subfield wise test sets
    # for idx, cate in enumerate(y_lbs):
    pred = classif.predict(X_test)
    cate_acc = confusion_matrix(y_test, pred, labels=y_lbs,normalize='true')
    for klass,acc in zip(y_lbs,cate_acc):
        print(klass, acc)

if __name__ == "__main__":
    abst_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_abstract_comp.txt'
    ft_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_ft_comp.txt'

    # abst_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs/cs_testcomp/cs_50_perdoc.txt'
    # ft_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs/model_50/composition.txt'

    abst_comp, ft_comp = read_data(abst_comp_path), read_data(ft_comp_path)
    CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
    cls_with_ft(train_df=ft_comp.iloc[:10000,:], test_df=abst_comp.iloc[:10000,:])
    print()

    # TODO
    # a lot of the test data
    # ABSOLUTE NUMBER OF PAPER 