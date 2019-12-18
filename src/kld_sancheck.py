from kldiv import read_data, get_div_dfs
from paths import data_path
from os.path import join
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
    # for df in [ftdf, secdf]:
    #     df.rename(columns={1:'pid'}, errors="raise", inplace=True)
    x = pd.merge(ftdf, secdf, on='pid',how='inner')
    new_ftdf = x.iloc[:, :101]
    new_secdf = pd.concat([x['pid'], x.iloc[:, 101:]], axis=1)
    return new_ftdf, new_secdf

def cp_abnormal_fulltext(oldft_path,newft_path,dst):
    pass

if __name__ == "__main__":
    ft_df = read_data(join(data_path,'old_topicmodel_data/full_nonstem_100_inf_props.txt'))
    secs_df = read_data(join(data_path,'old_topicmodel_data/secs_nonstem_100_props.txt'))
    abst_df = get_abst_df(secs_df)
    ft_df, abst_df = align_dfs(ft_df, abst_df)
    get_div_dfs(ft_df, abst_df, join(join(data_path, 'old_cs_abstract_kld.txt')), ['Computer_Science.xml'])