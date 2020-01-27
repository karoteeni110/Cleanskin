"""Evaluate topic models with multilabel classification"""
from kldiv import read_data, get_pid2cate_dict, align_dfs
from paths import results_path

from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.kernel_approximation import Nystroem
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import pandas as pd
import itertools
from os.path import join


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
    feature_mapper = Nystroem(gamma=.2,random_state=1,n_components=300)
    X_train = feature_mapper.fit_transform(X_train)
    print('Training...')
    classif = OneVsOneClassifier(LinearSVC(max_iter=100)).fit(X_train, y_train)
    
    print('Testing...')
    print()
    # GET subfield wise test sets
    subfields = set([i for l in CATEDICT.values() for i in l])
    test_df = dfpid2cate(test_df)
    print('subfield, # of test samples, accuracy')
    for sf in subfields:
        X_test, y_test = df2test(test_df, sf, le, y_train)
        X_test = feature_mapper.transform(X_test)
        if len(X_test) == 0:
            continue
        print(sf, len(X_test), classif.score(X_test, y_test))

def df2train_mlb(df):
    """"""
    mlb = MultiLabelBinarizer()    
    df.loc[:,'pid'] = df.pid.map(CATEDICT)
    df = df.dropna(subset=['pid']).sample(frac=1) # Drop those categories and shuffle
    df.loc[:,'pid'] = df.pid.apply(tuple)
    X_train = df.iloc[:,1:].to_numpy()
    y_train = mlb.fit_transform(df.pid)
    return X_train, y_train, mlb

def df2test_mlb(df, mlb, subfield):
    catedf = df.loc[df.pid.str.contains(subfield)]
    X_test = catedf.iloc[:,1:].to_numpy()
    catedf.loc[:,'pid'] = catedf['pid'].apply(lambda x: tuple(x.split(',')))
    y_test = mlb.transform(catedf.pid)
    return X_test, y_test

def one_vs_rest_clsf(train_df, test_df, results_dst=None):
    X_train, y_train, mlb = df2train_mlb(train_df)
    print('Training...')
    classif = OneVsRestClassifier(LinearSVC(verbose=1)).fit(X_train, y_train)
    # classif = RandomForestClassifier(verbose=1, n_jobs=2).fit(X_train, y_train)

    print('Testing...')
    print()
    test_df = dfpid2cate(test_df)
    results = pd.DataFrame(columns=['subfield', 'acc'])
    print('subfield, # of test samples, accuracy')
    for sf in mlb.classes_:
        X_test, y_test = df2test_mlb(test_df, mlb, sf)
        if len(X_test) == 0:
            continue
        sf_acc = classif.score(X_test, y_test)
        print(sf, len(X_test), sf_acc)
        results = results.append({'subfield':sf, 'acc':sf_acc}, ignore_index=True)
    print('macro-average acc:', results.acc.mean())
    if results_dst:
        results.to_csv(results_dst,index=False)
        print('Results at', results_dst)

if __name__ == "__main__":
    CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
    pd.options.mode.chained_assignment = None # Mute caveats
    
    
    for i in range(200,4200,200):
        ft_comp_path = '/cs/group/grp-glowacka/arxiv/models/cs_5ktpc/model_%d/fulltext_composition.txt' % i
        # abst_comp_path = '/home/ad/home/y/yzan/Desktop/Cleanskin/data/model_i_comp/model_200_abstract.txt'

        pd.options.mode.chained_assignment = None # Mute caveats
        # abst_comp = read_data(abst_comp_path,sepchar=',',skiprow=1,drop_first_col=False)
        ft_comp = read_data(ft_comp_path).sample(frac=1) # shuffle
        train_size = int(len(ft_comp)*0.8)
        one_vs_rest_clsf(train_df=ft_comp.iloc[:train_size,:],test_df=ft_comp.iloc[train_size:,:],\
            results_dst=join(results_path,'model/%dtpc_ft2ft_LSVCclf.txt' % i))
        print()

    # abst_comp = read_data(abst_comp_path,sepchar=',',skiprow=1,drop_first_col=False)
    # ft_comp = read_data(ft_comp_path)
    # X_train, y_train, mlb = df2train_mlb(ft_comp.sample(frac=0.01))
    # X_test, y_test = df2test_mlb(dfpid2cate(abst_comp).sample(frac=0.2), mlb, 'AI')
