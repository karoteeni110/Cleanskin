from paths import data_path, results_path
from os.path import join, exists, basename, dirname
from gensim.models import wrappers
from os import listdir
from newCleaner import get_root
import pickle
import matplotlib.pyplot as plt
import numpy as np


# Coherence
def read_diag(diag_xmlpath, metrics):
    """`model_dirpath`: .../<CATE_NAME>/model_NUM/diagnostics.xml
    `metrics`: attribute name
    Returns:
    num_of_topic (str); value: mean coherence value ()"""
    _, model = get_root(diag_xmlpath)
    m_values = []
    for topic in model:
        m_values.append(float(topic.get(metrics)))
    tpc_num, avgcoh = len(model), np.mean(m_values)
    return tpc_num, avgcoh

def get_alldiag(diag_xml_pathlst, metrics='coherence'):
    cate = diag_xml_pathlst[0].split('/')[-3]
    print('Reading', cate, 'diagnostics...')
    if exists(CATE_COH_PKLPATH):
        with open(CATE_COH_PKLPATH) as cate_coh_dict:
            cate_diag = pickle.load(cate_coh_dict)
    else:
        cate_diag = dict()
        for xmlpath in diag_xml_pathlst:
            model_tpc_num, avg_mv = read_diag(xmlpath, metrics)
            cate_diag[model_tpc_num] = avg_mv
        # cate = basename(diag_xml_pathlst)
        if DUMPDICT:
            pickle.dump(cate_diag, join(results_path, cate+'_'+metrics[:4]+'.pkl'))
    return cate_diag, metrics, cate

# Perplexity
def get_perp(evaltxt_path):
    """Returns: dict with single item 
    key: num_of_topics; value: probability AFTER log transformation"""
    pass

def get_allperp(eval_txt_pathlst):
    pass

def plot_data(datadict, metrics, cate):
    x, y = zip(*datadict.items())
    x, y = list(x), list(y)
    plt.plot(x, y)
    plt.xticks(x)
    plt.ylabel('Model '+metrics+' score')
    plt.xlabel('Num of topics')
    plt.title(cate.upper())
    # plt.axis([np.min(x), np.max(x), np.min(y), np.max(y)])
    plt.show()

if __name__ == "__main__":
    CATE_COH_PKLPATH = join(results_path, 'cs_coh.pkl')
    DUMPDICT = False
    modeldirx = '/cs/group/grp-glowacka/arxiv/models/physics/model_'

    diag_xmls = [join(modeldirx+str(tpcnum), 'diagnostics.xml') for tpcnum in range(50,1001,50)]
    cohdict, mt, c = get_alldiag(diag_xmls)
    plot_data(cohdict, mt, c)