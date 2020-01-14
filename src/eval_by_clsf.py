"""Evaluate topic models with multilabel classification"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import pandas as pd
import itertools
from kldiv import read_data, get_pid2cate_dict

def example():
    X, y = datasets.load_iris(return_X_y=True)
    # >>> OneVsOneClassifier(LinearSVC(random_state=0)).fit(X, y).predict(X)

def docdf2y(docdf):
    """https://scikit-learn.org/stable/modules/multiclass.html#multilabel-classification-format"""
    catedict = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
    cate_series = docdf.pid.map(catedict).to_list()
    # lb2idx = {cate:idx for idx,cate in enumerate(cates)}
    y = MultiLabelBinarizer().fit(catedict.values())
    return y

def cls_with_ft(ft_comp_df):
    X = ft_comp_df.iloc[:,1:].to_numpy()
    y = pid2y(doc_df.loc[:,'pid'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    

if __name__ == "__main__":
    abst_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_abstract_comp.txt'
    ft_comp_path = '/home/yzan/Desktop/mallet-2.0.8/cs_ft_comp.txt'

    abst_comp, ft_comp = read_data(abst_comp_path), read_data(ft_comp_path)
    cls_with_ft(ft_comp)
    print()
