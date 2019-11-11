import pandas as pd
import numpy as np
from newCleaner import get_root
from paths import data_path, results_path
from os.path import join, exists, basename
from gensim.models import wrappers
from os import listdir
import pickle
import matplotlib.pyplot as plt

def get_model_diag(xmlpat, metrics='coherence'):
    tpc, coh = '50', 0
    return tpc, coh

def plot_cate_diag(dirpath, metrics='coherence'):
    if exists(cate_coh_pklpath):
        with open(cate_coh_pklpath) as cate_coh_dict:
            cate_diag = pickle.load(cate_coh_dict)
    else:
        cate_diag = dict()
        models = listdir(dirpath)
        for md in models:
            pass
        cate = basename(dirpath)
        pickle.dump(cate_diag, join(results_path, cate+'_'+metrics+'.pkl'))
    plt(cate_diag)

def 

if __name__ == "__main__":
    # tpc50_df = read_data(join(data_path, 'cs_testcomp/cs_test_composition_50tpc.txt'))
    plot_cate_diag()