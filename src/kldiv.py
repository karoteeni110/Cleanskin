import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import xml.etree.ElementTree as ET
from newCleaner import get_root
from random import choice
from paths import kldiv_dir, data_path, metadatas_path
from metadata import get_pid2meta
from os.path import join
from os import listdir

def read_data(mallet_out):
    pd.set_option('precision', 21)
    print('Reading data: %s' % mallet_out)
    with open(mallet_out, 'r') as f:
        data = f.read().split('\n')
        first_line = data[0]
    if first_line[0] == '0': 
        df = pd.read_csv(mallet_out, sep="\t", header=None, float_precision='high').drop(0,axis=1)
    else:
        df = pd.read_csv(mallet_out, skiprows=1, sep="\t", header=None, float_precision='high').drop(0, axis=1)

    # Strip file extension
    if '/' in df.iloc[1,0] and df.iloc[1,0][-4:]=='.txt': 
        print('Stripping extention name in pid...')
        df.loc[:,1] = df.loc[:,1].apply(lambda x:x.split('/')[-1][:-4]) 
        print('... done')

    # df.iloc[:,1:].to_list()
    df = df.rename(columns={1:'pid'})
    return df

def get_pid2cate_dict(metaxml_list):
    """TODO: repeat article n times; n=len(category)"""
    pid2meta = get_pid2meta(metaxml_list)
    pid2cates = dict()
    for pid in pid2meta:
        pid2cates[pid] = [c[3:] for c in pid2meta[pid]['categories'].split(', ') 
                            if c[:2]=='cs']
        # pid2cate[pid] = choice([c[3:] 
        #     for c in pid2meta[pid]['categories'].split(', ') 
        #         if c[:2]=='cs'])
    return pid2cates

def acro_trans(cate_series):
    _, root = get_root(join(data_path, 'cs_cate_acro.xml'))
    acro2cate = dict()
    for i in range(len(root)):
        if i%2==1:
            # ET.dump(root[i][0][0])
            # print(root[i][0][0].text)
            acro, fn = root[i][0][0].text.split(' - ')
            fn = re.sub(r'\s\(.*\)','',fn) #remove parenthese
            acro2cate[acro] = fn
    return cate_series.map(acro2cate)

def get_div_dfs(fulltext_df, sec_df, dst, metaxml_list=listdir(metadatas_path)):
    """ 
    """
    if fulltext_df.iloc[:,0].equals(sec_df.iloc[:,0]) and fulltext_df.shape==sec_df.shape: # pids must be aligned

        # Compute KLdiv
        p_i, q_i = fulltext_df.iloc[:,1:].to_numpy(), sec_df.iloc[:,1:].to_numpy()
        kldiv_i = np.multiply(p_i, np.log2(p_i)-np.log2(q_i)) # element-wise multiply
        kldiv_paper = np.sum(kldiv_i,axis=1) #.reshape((-1,1))
        
        div_df = pd.concat([fulltext_df.pid, pd.Series(kldiv_paper, name='kld')], axis=1)

        catedict = get_pid2cate_dict(metaxml_list)
        cate_series = fulltext_df.pid.map(catedict)# .apply(pd.Series) # fill with NaN 
        div_df = cate_series.merge(div_df, left_index=True, right_index=True) \
                    .melt(id_vars=['pid','kld'], value_name='category') \
                    .drop('variable',axis=1) \
                    .dropna()
        # div_df.insert(1,'cates',cate_series) # add


        # cate_series = acro_trans(cate_series)
        
        # print('Paper category not found:') 
        # print(fulltext_df[cate_series.isnull()])
        # print('Check if uncategorized are all from 2019:')
        # print(fulltext_df[cate_series.isnull()].iloc[:,1].str.match(pat='1907.*').sum())
        # exit(0)

        # div_df.columns = ['pid', 'kld', 'category']
        div_df = div_df[div_df['category'].notnull()]  # exclude cases where categories not found
        div_df.to_csv(path_or_buf=dst, index=False)
        print('KLD stats DONE! %s' % dst)
        # return div_df
    else:
        print('DFs not aligned.')
        print('Full-text pids:', fulltext_df.loc[:,1])
        print('Sec pids:', sec_df.loc[:,1])
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
    get_div_dfs(ft_df, abt_df, join(data_path, 'cs_abstract_kld.txt'), ['Computer_Science.xml'])
    # acro_trans(0)