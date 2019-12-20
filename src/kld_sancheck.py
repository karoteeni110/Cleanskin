from kldiv import read_data, get_div_dfs
from paths import data_path, results_path
from os.path import join, basename, dirname
from os import listdir
from shutil import copyfile
import pandas as pd
import numpy as np

def get_abst_df(secs_df):
    print('Extracting abstract composition...')

    # Pick those title=='abstr'
    abst_ids = pd.read_csv(join(data_path, 'old_topicmodel_data/section_titles.txt'), header=0)
    abst_ids = abst_ids[abst_ids.title=='abstr'].iloc[:,0].tolist()
    abst_df = secs_df[secs_df.pid.isin(abst_ids)]
    
    if abst_df.iloc[0,0][-2:] == '_0':
        print('Stripping _0 in pid...')
        abst_df.pid = abst_df.pid.map(lambda x:x[:-2]) # strip '_0' in filename
    return abst_df

def align_dfs(ftdf,secdf):
    """not in use"""
    x = pd.merge(ftdf, secdf, on='pid',how='inner')
    new_ftdf = x.iloc[:, :101]
    new_secdf = pd.concat([x['pid'], x.iloc[:, 101:]], axis=1)
    return new_ftdf, new_secdf

def word_count(txtpath):
    with open(txtpath, 'r') as f:
        words = f.read().strip().split()
    return len(words)

def cp_abnormal_fulltext(oldft_path,newft_path):
    wc1, wc2 = word_count(oldft_path), word_count(newft_path)
    diff = wc1 - wc2
    txtname = basename(newft_path)
    if diff != 0:
        print('%d, %s' % (diff, txtname))
        copyfile(newft_path, '/home/yzan/Desktop/cs_lda/abst_diff/new_%s' % txtname)
        copyfile(oldft_path, '/home/yzan/Desktop/cs_lda/abst_diff/old_%s' % txtname)
        print()
        return True
        

if __name__ == "__main__":
    # ft_df = read_data('/home/yzan/Desktop/cs_lda/topicmodel_data/full_nonstem_100_inf_props.txt')
    # secs_df = read_data('/home/yzan/Desktop/cs_lda/topicmodel_data/secs_nonstem_100_props.txt')
    # abst_df = get_abst_df(secs_df)
    # get_div_dfs(ft_df, abst_df, join(join(data_path, 'rerun_old_cs_abstract_kld.txt')), ['Computer_Science.xml'])
    # print()

    # newftdir = join(results_path, 'cs_lbsec/abstract')
    # oldftdir = '/home/yzan/Desktop/cs_lda/abstract'
    # for fttxt in listdir(newftdir):
    #     newft_path = join(newftdir, fttxt)
    #     oldft_path = join(oldftdir, fttxt)
    #     if fttxt in []:
    #         continue
    #     if cp_abnormal_fulltext(oldft_path,newft_path):
    #         pass

    abst_ids = pd.read_csv(join(data_path, 'old_topicmodel_data/section_titles.txt'), header=0)
    abst_ids = abst_ids[abst_ids.title=='abstr'].iloc[:,0].str.replace('_0','')# .tolist()
  
    whatif = pd.read_csv('/home/yzan/Desktop/scilit_graphs/redoredoabst.csv',header=0)
    whatif = whatif[whatif.pid.isin(abst_ids)]
    print()