import pandas as pd
from itertools import combinations
from os import listdir
from os.path import join

def read_topic_file(fpath):
    tpcs = []
    with open(fpath,'r') as f:
        for line in f.readlines():
            tpcset = line.split()[-1].split(',')
            tpcs.append(tpcset)
    return tpcs


def merge_topics():
    all_models = []
    grp_dir ='/cs/group/grp-glowacka/arxiv/models/cs_gensim/30x100_results'
    for fn in listdir(grp_dir):
        if 'topics' in fn:
            fpath = join(grp_dir, fn)
            all_topics.extend(fpath)
    
    for topic_1a in model1_topics:
        for topic_2a in model2 topics:
            if topic_1a.intersect(topic_2a)


if __name__ == "__main__":
    pass