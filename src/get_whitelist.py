import pandas as pd
import numpy as np
from os import listdir
from kldiv import get_pid2cate_dict, get_acro2cate_dict
import matplotlib.pyplot as plt

CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])
acro2cate = get_acro2cate_dict()

def cate_count(catelist):
    a = np.concatenate(catelist.cate.to_numpy())
    a = pd.Series(a)
    return a.value_counts()

def data_barplot(ft_df):
    # ft_df = read_data('/cs/group/grp-glowacka/arxiv/models/cs_5ktpc/model_200/fulltext_composition.txt')
    # ft_df = pd.read_csv('/home/yzan/Desktop/trypid.txt', 
    #         sep='\n', names=['pid'])
    acro2cate = get_acro2cate_dict()
    catelist_forcount = np.concatenate(ft_df.pid.map(CATEDICT).dropna().to_numpy())
    a=pd.Series(catelist_forcount).map(acro2cate)
    print(a.value_counts())

def main(threshold):
    print('Reading pids...')
    ft_df = pd.read_csv('/Users/Karoteeni/coooode/Cleanskin/gensim_results/whitelist_3000.txt',header=None,names=['pid'])
    #     .drop(['kld','category'],axis=1)\
    #         .drop_duplicates()
    # ft_df = pd.DataFrame(listdir('/home/ad/home/y/yzan/Desktop/Cleanskin/results/cs_lbsec/cs_ft'), 
            #    columns=['pid'])\
    #                .apply(lambda x: x[0][:-4],axis=1,result_type='broadcast')
    ft_df = ft_df.sample(frac=1)
    catelist = pd.concat([ft_df, ft_df.pid.map(CATEDICT).rename('cate')],axis=1).dropna()
    cate_freq = cate_count(catelist)
    # ml = catelist[catelist.cate.apply(lambda x: 'LG' in x)]


    while len(cate_freq[cate_freq>threshold]) > 0:
        cate_to_sample = cate_freq.index[cate_freq>threshold][0] # the most frequent cate
        how_many = cate_freq[cate_to_sample]
        remove_n = np.min([how_many-threshold, 1000]) # Remove papers slowly: incre = 1000
        cate_blacklist_idx = catelist[catelist.cate.apply(lambda x: cate_to_sample in x)].sample(n=remove_n).index
        catelist = catelist.drop(cate_blacklist_idx) # update catelist
        cate_freq = cate_count(catelist)# update cate_freq
        print()

    catelist.pid.to_csv('whitelist_%s.txt' % threshold, index=False, header=False)


if __name__ == "__main__":
    main(threshold=3000)