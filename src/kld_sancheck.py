from kldiv import read_data, get_div_dfs
from paths import data_path
from os.path import join
import pandas as pd
import numpy as np

def get_abst_df(secs_df):
    print('Extracting abstract composition...')
    abst_ids = pd.read_csv(join(data_path, 'old_topicmodel_data/section_titles.txt'), header=0)
    abst_ids = abst_ids[abst_ids.title=='abstr'].iloc[:,0].tolist()
    abst_select = secs_df[1].isin(abst_ids)
    abst_df = secs_df[abst_select]
    if abst_df.iloc[0,0][-2:] == '_0':
        print('Stripping _0 in pid...')
        pids = abst_df.iloc[:,0].copy()
        abst_df.loc[:,1] = pids.apply(lambda x:x[:-2]) # strip '_0' in filename
    return abst_df

def align_dfs(ftdf,secdf):
    for df in [ftdf, secdf]:
        df.rename(columns={1:'pid'}, errors="raise", inplace=True)
    # print(pd.merge(ftdf, secdf, on='pid', how='right'))
    x = pd.merge(ftdf, secdf, on='pid',how='inner')
    new_ftdf = x.iloc[:, :101]
    new_secdf = pd.concat([x['pid'], x.iloc[:, 101:]], axis=1)

    # new_ftdf = ftdf[ftdf.iloc[:,1].isin(secdf.iloc[:,1]).tolist()]
    # new_ftdf = new_ftdf.sort_values(by=1)
    # new_secdf = secdf.sort_values(by=1)
    # print(new_ftdf)
    # print(new_secdf)
    return new_ftdf, new_secdf

    # print(ftdf.loc[:,1].equals(secdf.loc[:,1]))

if __name__ == "__main__":
    ft_df = read_data(join(data_path,'old_topicmodel_data/full_nonstem_100_inf_props.txt'))
    secs_df = read_data(join(data_path,'old_topicmodel_data/secs_nonstem_100_props.txt'))
    abst_df = get_abst_df(secs_df)
    align_dfs(ft_df, abst_df)
    # get_div_dfs(ft_df, abst_df, join(join(data_path, 'old_cs_abstract_kld.txt')), ['Computer_Science.xml'])