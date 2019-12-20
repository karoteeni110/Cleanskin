import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import xml.etree.ElementTree as ET
from newCleaner import get_root
from random import choice
from paths import kldiv_dir, data_path,metadatas_path,secklds,results_path
from metadata import get_pid2meta
from os.path import join, basename
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

def get_pid2cate_dict(metaxml_list=listdir(metadatas_path), random_cate=False):
    """returns dictionary: 
    key:pid str; value: list of category acronyms"""
    pid2meta = get_pid2meta(metaxml_list)
    pid2cates = dict()
    for pid in pid2meta:
        if not random_cate:
            pid2cates[pid] = [c[3:] for c in pid2meta[pid]['categories'].split(', ') 
                            if c[:2]=='cs']
        else:
            pid2cates[pid] = choice([c[3:] for c in pid2meta[pid]['categories'].split(', ') 
                            if c[:2]=='cs'])
    return pid2cates

def get_acro2cate_dict():
    """returns a dictionary, keys: acronyms, values: human-readable categories"""
    _, root = get_root(join(data_path, 'cs_cate_acro.xml'))
    acro2cate = dict()
    for i in range(len(root)):
        if i%2==1:
            # ET.dump(root[i][0][0])
            # print(root[i][0][0].text)
            acro, fn = root[i][0][0].text.split(' - ')
            fn = re.sub(r'\s\(.*\)','',fn) #remove parenthese
            acro2cate[acro] = fn
    return acro2cate # cate_series.map(acro2cate)

def align_dfs(ft_df,sec_df, n_tpc=100):
    innerjoin = pd.merge(ft_df, sec_df, how='inner', on='pid')
    ft_df = innerjoin.iloc[:,:n_tpc+1]\
            .rename(columns = lambda x:x.strip('_x'))
    sec_df = pd.concat([innerjoin.iloc[:,0],innerjoin.iloc[:, n_tpc+1:]], axis=1)\
            .rename(columns = lambda x:x.strip('_y'))

    return ft_df, sec_df

def get_div_dfs(fulltext_df, sec_df, dst, metaxml_list=listdir(metadatas_path)):
    """ 
    """
    fulltext_df, sec_df = align_dfs(fulltext_df, sec_df)
    if fulltext_df.iloc[:,0].equals(sec_df.iloc[:,0]) and fulltext_df.shape==sec_df.shape: # pids must be aligned
        print("Dataframes aligned. Calculating KLdiv...")
        # Compute KLdiv
        p_i, q_i = fulltext_df.iloc[:,1:].to_numpy(), sec_df.iloc[:,1:].to_numpy()
        kldiv_i = np.multiply(p_i, np.log2(p_i)-np.log2(q_i)) # element-wise multiply
        kldiv_paper = np.sum(kldiv_i,axis=1) #.reshape((-1,1))
        
        div_df = pd.concat([fulltext_df.pid, pd.Series(kldiv_paper, name='kld')], axis=1)

        catedict = get_pid2cate_dict(metaxml_list)
        cate_series = fulltext_df.pid.map(catedict).apply(pd.Series) # fill with NaN 
        # Repeat each paper n times (n=len(categories)) 
        div_df = cate_series.merge(div_df, left_index=True, right_index=True) \
                    .melt(id_vars=['pid','kld'], value_name='category') \
                    .drop('variable',axis=1) \
                    .dropna()        

        div_df.category = div_df.category.map(get_acro2cate_dict()) # Human-readable categories
        # print('Categories not found:', len(div_df.category.isnull()))
        div_df = div_df[div_df.category.notnull()]
        div_df = div_df.loc[ ~(div_df['category'].str.match(r'(General Literature|Other)')) ]
        
        div_df.to_csv(path_or_buf=dst, index=False)
        print('KLD stats DONE! %s' % dst)
        # return div_df
    else:
        print('DFs not aligned.')
        print('Full-text pids:')
        print(fulltext_df.pid)
        print('Sec pids:')
        print(sec_df.pid)
        exit(0)

def show_errbar():
    """ABANDONED"""
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
    """ABANDONED"""
    _, ax = plt.subplots()
    x = ['one', 'two', 'three']
    y = ['two', 'three', 'four']
    l = [1, 2, 3]

    ax.plot(l,y)
    # ax.set_xticks(l)
    ax.set_yticklabels(x)
    plt.show()

def read_sectionKLD_df(txtpath, dfname=False):
    """Read pd.dataframe from txt file
    Take first row as header
    df.name depends on filename: df.name = re.search(fn, '_(\\w+)_kld.txt')"""
    df = pd.read_csv(txtpath, header=0)
    if not dfname:
        df.name = re.search(r'_(\w+)_kld.txt',basename(txtpath)).group(1)
    else:
        df.name = dfname
    return df

def get_sec_structure_vecs(all_secdf_dict, dst=False):
    """
    Compute section-structure vectors, returns in pd.dataframe
    Columns:  
    name,Abstract,Introduction,Background,Related Work,Methods,Results,Discussion,Conclusion
    name: subfields of the subject.
        For CS, name = []'machine_learning', 'numerical_analysis', ...
    """
    # Initialisation
    abst_df = all_secdf_dict['abstract']
    name = abst_df.category.unique()
    secvec_df = pd.DataFrame({'name':name})

    # Fill in dataframe cell by cell
    for sec in ['abstract','introduction','background','relatedwork','methods','results','discussion','conclusion']:
    # for sec in all_secdf_dict: # col
        print("Getting",sec,"vectors...")
        col = []
        for field in secvec_df.name: # row
            seckld = all_secdf_dict[sec]
            col.append(seckld[seckld.category==field]['kld'].mean())
        secvec_df[sec] = col
        print("... done")
    
    secvec_df.columns = secvec_df.columns.str.title()
    secvec_df = secvec_df.rename(columns={'Relatedwork':'Related Work', 'Name':'name'})

    if not dst:
        return secvec_df
    else:
        secvec_df.to_csv(path_or_buf=dst, index=False)
        return secvec_df

if __name__ == "__main__":
    #ft_df = read_data(join(data_path, '100tp_sec_compo/cs_ft_comp_100tpc.txt'))
    #abt_df = read_data(join(data_path, '100tp_sec_compo/cs_abt_composition_100tpc.txt'))
    # get_div_dfs(ft_df, abt_df, join(data_path, 'cs_sec_klds/cs_abstract_kld.txt'), ['Computer_Science.xml'])
    
    # ft_df = read_data('/home/yzan/Desktop/mallet-2.0.8/cs_ft_composition_100tpc_2.txt')
    # abt_df = read_data('/home/yzan/Desktop/mallet-2.0.8/cs_abt_compo2.txt')
    # get_div_dfs(ft_df, abt_df, '/home/yzan/Desktop/mallet-2.0.8/abt_kld2.txt',['Computer_Science.xml'])
    
    ft_df = read_data('/home/yzan/Desktop/mallet-2.0.8/cs_ft_comp.txt')
    abt_df = read_data('/home/yzan/Desktop/mallet-2.0.8/cs_abt_comp.txt')
    get_div_dfs(ft_df, abt_df, '/home/yzan/Desktop/mallet-2.0.8/abtkld.txt',['Computer_Science.xml'])

    # all_sec_dfs = dict()  
    # for txtfn in listdir(secklds):
    #     if 'abstract' not in txtfn:
    #         secdf = read_sectionKLD_df(join(secklds, txtfn))
    #     else:
    #         secdf = read_sectionKLD_df('/home/yzan/Desktop/Mallet/abt_kld2_fromdev.txt', dfname='abstract')
    #     all_sec_dfs[secdf.name] = secdf
    # get_sec_structure_vecs(all_sec_dfs,dst = '/home/yzan/Desktop/scilit_graphs/secvec_fromdev.txt')# dst=join(results_path, 'my_secvec.txt'))