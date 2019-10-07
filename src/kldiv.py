import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from random import choice
from paths import kldiv_dir, data_path
from os.path import join

def read_data(mallet_out):
    pd.set_option('precision', 21)
    df = pd.read_csv(mallet_out, sep="\t", header=None, float_precision='high')
    df[1] = df[1].apply(lambda x:x.split('/')[-1][:-4]) # strip file extension
    # print(df.head(3))
    return df.head(3)

def get_pid2cate_dict(catedata_path):
    pid2cate = dict()
    with open(catedata_path, 'r') as catef:
        for line in catef:
            raw_pid, raw_cates = line.split('')
            pid = re.sub(r'//', '', raw_pid) # quant-ph/9904108 => quant-ph9904108
            rand_subcate = choice([c[3:] for c in raw_cates.split(',') if c[:2]=='cs'])
            pid2cate[pid] = rand_subcate
    return pid2cate

def merge_frames(df1, df2):
    return 0

def get_div_dfs(fulltext_df, sec_df):
    """ 
    """
    if fulltext_df.loc[:,1].equals(sec_df.loc[:,1]): # pids must be aligned
        p_i, q_i = fulltext_df.iloc[:,2:].to_numpy(), sec_df.iloc[:,2:].to_numpy()
        kldiv_i = np.multiply(p_i, np.log2(p_i)-np.log2(q_i)) # before sum
        kldiv_paper = np.sum(kldiv_i,axis=1).reshape((-1,1))
        cate_vec = get_pid2cate_dict(CATEDATA_PATH)
        pid_with_cate = merge_frames(fulltext_df.iloc[:, :3], cate_vec)
        div_df = merge_frames(pid_with_cate, kldiv_paper)
        return div_df
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
    CATEDATA_PATH = join(data_path, 'arxiv_cate/Computer_Science.txt')
    get_div_dfs(ft_df, abt_df)