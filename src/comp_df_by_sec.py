"""Extract section-wise compositions from secs_comp.txt 
    and write out the dataframe to secname.txt"""
import pandas as pd
import numpy as np
import pickle
from paths import f_sectitles, data_path, src_path
from sortLabels import final
from os.path import join, basename
from os import listdir

def read_sec_hdings(sec_titles):
    """`sec_titles` - the path to secs_titles.txt"""
    print('Reading data: %s' % sec_titles)
    df = pd.read_csv(sec_titles, sep=r'^([^,]+),', engine='python', header=None, dtype=str).drop(0,axis=1) # sep= the first comma
    df = df.rename(columns={1:'fn', 2:'heading'})
    df = df.dropna() # Remove the sections with empty heading
    print('... done')
    return df

def read_sec_comp(mallet_out):
    """Read mallet output: sec compositions"""
    pd.set_option('precision', 21)
    print('Reading data: %s' % mallet_out)
    # with open(mallet_out, 'r') as f:
    #     data = f.read().split('\n')
    #     first_line = data[0]
    # if first_line[0] == '0': 
    #     df = pd.read_csv(mallet_out,sep="\t",header=None,float_precision='high').drop(0,axis=1)
    # else:
    df = pd.read_csv(mallet_out,skiprows=1,sep="\t",header=None,float_precision='high').drop(0, axis=1)

    # Strip file extension
    if '/' in df.iloc[1,0] and df.iloc[1,0][-4:]=='.txt': 
        print('Stripping dirpath in fn...')
        df.loc[:,1] = df.loc[:,1].apply(lambda x:basename(x)) 
        print('... done')

    # df.iloc[:,1:].to_list()
    df = df.rename(columns={1:'fn'})
    return df

def extract_abst(bigdf, dst=join(data_path,'abst_fname.txt'), writeout=False):
    sec = 'abstract'
    print('Extracting %s fnames...' % sec)
    df = bigdf[bigdf.heading.str.match(sec)]

    if writeout:
        print('Writing out %s to %s' % (sec, dst))
        df.to_csv(path_or_buf=dst, index=False)

def extract_othercate(bigdf, dst, writeout=False):
    print('Extracting intro, background etc fnames...')
    df = pd.concat([bigdf.fn,bigdf.heading.map(final).rename('cate')],axis=1).dropna()
    # for cate in ['introduction','related_work','background','methods','results','discussion','conclusion']:
    if writeout:
        print('Writing out %s to %s' % ('useful sections', dst))
        df.to_csv(path_or_buf=dst, index=False)

def subset_fn(fndf, catename):
    return fndf[fndf.heading.apply(lambda a: catename in a)].fn[1:].to_list()

def except_abst_fn(fndf):
    return fndf[fndf.heading.apply(lambda a: 'abstract' not in a)].fn[1:].to_list()

def extract_documents(dirn, fnlist):
    ids = []
    docs = []
    print('Reading documents...')
    for i,fname in enumerate(fnlist):
        fpath = join(dirn, fname)
        pid = fname.split('_')[0]

        ids.append(pid)
        doc = []
        with open(fpath) as f :
            doc = f.read().encode('utf-8', errors='replace').decode()
            docs.append(doc)

        if (i+1)%1000==0:
            print(i+1,'/', len(fnlist), '...')
    return ids,docs

def subset_from_secs_comp(secs_comp, fns):
    print('Subsetting...')
    subset = pd.merge(fns, secs_comp, how='left', on='fn').drop('heading',axis=1).drop(0,axis=0)
    # subset.loc['fn'] = subset.loc['fn'].apply(lambda x: x.split('_')[0])
    print('... done')
    return subset

if __name__ == "__main__":
    # bigdif = read_sec_hdings(join(data_path,'sec_titles.txt'))
    # abst_fns = read_sec_hdings(join(data_path, 'abstract_fname.txt'))
    allcatefn = read_sec_hdings(join(data_path, 'catesec_fname.txt'))
    # for cate in ['introduction','related_work','background','methods','results','discussion','conclusion']:
    nonabst_cate_fns = except_abst_fn(allcatefn)
    cate_ids, cate_docs = extract_documents('/home/ad/home/y/yzan/Desktop/Cleanskin/results/cs_lbsec/sections', nonabst_cate_fns)
    try:
        with open('./cs_extract_nonabst_cate_130k','wb') as f:
            pickle.dump([cate_ids,cate_docs],f)
    except MemoryError:
        print('memory error')

    print()
    # nonabst_cate_fname = extract_sec(bigdif, dst=join(data_path, 'nonabst_cate_fname.txt'),sec)

    # # 
    # # for model_i in listdir(models_path):
    # #     if model_i[:6] == 'model_' and model_i not in ['model_200', 'model_400']:
    # secs_comp_df = read_sec_comp(join(src_path, 'KLDiv/10_1_abstract_composition.txt'))
    # # secdf = subset_from_secs_comp(secs_comp_df, abst_fns)
    # dst = join(data_path, 'model_i_comp/'+model_i+'_abstract.txt')
    # secdf.to_csv(path_or_buf=dst, index=False)
    # print(model_i, 'to', dst)

