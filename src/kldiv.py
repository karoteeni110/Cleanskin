import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data(datafile):
    pd.set_option('precision', 21)
    df = pd.read_csv(datafile, sep="\t", header=None, float_precision='high')
    df[1] = df[1].apply(lambda x:x.split('/')[-1][:-4]) # strip file extension
    print(df.head(3))
    # return df

def align_dfs(df1,df2):
    return 0

def merge_frames(df1, df2):
    return 0

def get_div_dfs(fulltext_df, sec_df):
    """ 
    """
    align_dfs(fulltext_df, sec_df)
    p_i = fulltext_df.iloc[:,2:] 
    q_i = sec_df.iloc[:, 2:]
    kl_divs = np.multiply(p_i, np.log2(p_i)-np.log2(q_i))
    cate_vec = 0
    pid_with_cate = merge_frames(fulltext_df.iloc[:, :3], cate_vec)
    div_df = merge_frames(pid_with_cate, kl_divs)
    return div_df

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
    read_data('./KLdiv/cs_ft_composition.txt')
    # ft_df, abt_df = read_data('./KLdiv/cs_ft_composition.txt'), read_data('./KLdiv/cs_abs_composition.txt')
    # kl_df = get_kldf(ft_df, abt_df)