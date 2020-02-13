import pandas as pd
import numpy as np
from os import listdir
from kldiv import get_pid2cate_dict, get_acro2cate_dict

CATEDICT = get_pid2cate_dict(metaxml_list=['Computer_Science.xml'])

def cate_count(catelist):
    a = np.concatenate(catelist.cate.to_numpy())
    a = pd.Series(a)
    return a.value_counts()

def main(threshold):
    print('Reading pids...')
    ft_df = pd.DataFrame(listdir('/home/ad/home/y/yzan/Desktop/Cleanskin/results/cs_lbsec/cs_ft'), 
                columns=['pid'])\
                    .apply(lambda x: x[0][:-4],axis=1,result_type='broadcast')
    ft_df = ft_df.sample(frac=1)
    catelist = pd.concat([ft_df, ft_df.pid.map(CATEDICT).rename('cate')],axis=1).dropna()
    cate_freq = cate_count(catelist)
    a=cate_count(pd.concat([ft_df,ft_df.pid.map(CATEDICT).rename('cate')],axis=1).dropna())

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