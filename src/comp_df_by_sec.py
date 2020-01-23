"""Extract section-wise compositions from secs_comp.txt 
    and write out the dataframe to secname.txt"""
import pandas as pd
import numpy as np
from paths import f_sectitles, data_path
from os.path import join

def read_sec2hd(mallet_out):
    """
    Param: `mallet_out` - the path to secs_comp.txt 
    the same func as in kldiv.py"""
    print('Reading data: %s' % mallet_out)
    df = pd.read_csv(mallet_out, sep=r'^([^,]+),', engine='python', header=None, dtype=str).drop(0,axis=1) # sep= the first comma
    # Strip file extension
    # if '/' in df.iloc[1,0] and df.iloc[1,0][-4:]=='.txt': 
    #     print('Stripping extention name in pid...')
    #     df.loc[:,1] = df.loc[:,1].apply(lambda x:x.split('/')[-1][:-4]) 
    #     print('... done')
    # df.iloc[:,1:].to_list()
    df = df.rename(columns={1:'fn', 2:'heading'})
    df = df.dropna() # Remove the sections with empty heading
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

if __name__ == "__main__":
    bigdf = read_sec2hd(join(data_path, 'abstract_fname.txt'))
    print(bigdf.loc[121])
