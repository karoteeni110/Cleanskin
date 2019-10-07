import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from random import choice
from paths import kldiv_dir, data_path, metadatas_path
from metadata import get_urlid2meta
from os.path import join
from os import listdir

def read_data(mallet_out):
    pd.set_option('precision', 21)
    df = pd.read_csv(mallet_out, sep="\t", header=None, float_precision='high')
    df[1] = df[1].apply(lambda x:x.split('/')[-1][:-4]) # strip file extension
    # print(df.head(3))
    return df

def get_pid2cate_dict(metaxml_list):
    pid2meta = get_urlid2meta(metaxml_list)
    pid2cate = dict()
    for pid in pid2meta:
        pid2cate[pid] = choice([c[3:] 
            for c in pid2meta[pid]['categories'].split(', ') 
                if c[:2]=='cs'])
    return pid2cate

def merge_frames(df1, df2):
    return 0

def get_div_dfs(fulltext_df, sec_df, metaxml_list=listdir(metadatas_path)):
    """ 
    """
    if fulltext_df.loc[:,1].equals(sec_df.loc[:,1]): # pids must be aligned
        p_i, q_i = fulltext_df.iloc[:,2:].to_numpy(), sec_df.iloc[:,2:].to_numpy()
        kldiv_i = np.multiply(p_i, np.log2(p_i)-np.log2(q_i)) # before sum
        kldiv_paper = np.sum(kldiv_i,axis=1) #.reshape((-1,1))
        cate_series = fulltext_df.iloc[:,1].map(get_pid2cate_dict(metaxml_list))

        # exclude cases where categories not found
        cate_series, fulltext_df = cate_series[cate_series.notnull()], fulltext_df[cate_series.notnull()] 
        # print('Paper category not found:') 
        # print(fulltext_df[cate_series.isnull()])
        # print('Check if uncategorized are all from 2019:')
        # print(fulltext_df[cate_series.isnull()].iloc[:,1].str.match(pat='1907.*').sum())
        # exit(0)
        div_df = pd.concat([fulltext_df.iloc[:, 1:2], cate_series, pd.Series(kldiv_paper)], axis=1)
        # colnames = pd.Series(['pid', 'category', 'kld']) 
        # div_df = div_df.assign(column_name=colnames)
        print(div_df.head(10))
        # return div_df
    else:
        print('DFs not aligned')
        exit(0)

def show_errbar():
    # plt.style.use('seaborn-whitegrid')
    y = np.linspace(0, 4, 3)  # categories, str
    dx = 0.8
    x = dx * np.random.randn(3)
    plt.xlabel('KL divergence (bits)')
    
    # plt.yticks(np.array([4]), ('four'))
    locs, labels = plt.yticks()
    print(locs, labels)
    plt.errorbar(x, y, xerr=dx, fmt='.k') #, color='black')

    plt.show()

def ytick():
    _, ax = plt.subplots()
    x = ['one', 'two', 'three']
    y = ['two', 'three', 'four']
    l = [1, 2, 3]

    ax.plot(l,y)
    # ax.set_xticks(l)
    ax.set_yticklabels(x)
    plt.show()

if __name__ == "__main__":
    # ytick()
    # show_errbar()
    ft_df = read_data(join(kldiv_dir, 'cs_ft_composition.txt'))
    abt_df = read_data(join(kldiv_dir, 'cs_abt_composition.txt'))
    # print(ft_df)
    # print()
    # print(abt_df)
    get_div_dfs(ft_df, abt_df, ['Computer_Science.xml'])