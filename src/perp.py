import pandas as pd
import numpy as np
from kldiv import read_data
from paths import data_path
from os.path import join

def logarize(df):
    return df.apply(lambda x:x.apply(log()))

if __name__ == "__main__":
    tpc50_df = read_data(join(data_path, 'cs_testcomp/cs_test_composition_50tpc.txt'))
    
    print()