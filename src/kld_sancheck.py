from kldiv import read_data, get_div_dfs
from paths import data_path
from os.path import join
import pandas as pd
import numpy as np

def get_abst_df(secs_df):
    print('Extracting abstract composition...')
    abst_ids = pd.read_csv(join(data_path, 'old_topicmodel_data/section_titles.txt'), header=0)
    abst_ids = abst_ids[abst_ids.title=='abstr'].iloc[:,0].tolist()
    abst_select = secs_df.iloc[:,1].isin(abst_ids)
    
    abst_df = secs_df[abst_select]
    if abst_df.iloc[1,1][-2:] == '_0':
        print('Stripping _0 in pid...')
        abst_df.loc[:,1] = abst_df.iloc[:,1].apply(lambda x:x[:-2]) # strip '_0' in filename
    return abst_df

if __name__ == "__main__":
    ft_df = read_data(join(data_path,'old_topicmodel_data/full_nonstem_100_inf_props.txt'))
    secs_df = read_data(join(data_path,'old_topicmodel_data/secs_nonstem_100_props.txt'))
    abst_df = get_abst_df(secs_df)
    get_div_dfs(ft_df, abst_df, join(join(data_path, 'old_cs_abstract_kld.txt')), ['Computer_Science.xml'])