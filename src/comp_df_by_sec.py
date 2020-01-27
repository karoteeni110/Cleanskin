"""Extract section-wise compositions from secs_comp.txt 
    and write out the dataframe to secname.txt"""
import pandas as pd
import numpy as np
from paths import f_sectitles, data_path, models_path
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

def extract_sec(bigdf, dst=join(data_path,'abst_fname.txt'), sec='abstract', writeout=False):
    if sec=='abstract':
        print('Extracting %s fnames...' % sec)
        df = bigdf[bigdf.heading.str.match(sec)]
    else:
        pass
    if writeout:
        print('Writing out %s to %s' % (sec, dst))
        df.to_csv(path_or_buf=dst, index=False)

def subset_from_secs_comp(secs_comp, fns):
    print('Subsetting...')
    subset = pd.merge(fns, secs_comp, how='left', on='fn').drop('heading',axis=1).drop(0,axis=0)
    # subset.loc['fn'] = subset.loc['fn'].apply(lambda x: x.split('_')[0])
    print('... done')
    return subset

if __name__ == "__main__":
    abst_fns = read_sec_hdings(join(data_path, 'abstract_fname.txt'))
    for model_i in listdir(models_path):
        if model_i[:6] == 'model_' and model_i not in ['model_200', 'model_400']:
            secs_comp_df = read_sec_comp(join(models_path, model_i)+'/secs_comp.txt')
            secdf = subset_from_secs_comp(secs_comp_df, abst_fns)
            dst = join(data_path, 'model_i_comp/'+model_i+'_abstract.txt')
            secdf.to_csv(path_or_buf=dst, index=False)
            print(model_i, 'to', dst)
    
