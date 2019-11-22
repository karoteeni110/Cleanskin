from paths import data_path, results_path
from os.path import join, exists, basename, dirname
from gensim.models import wrappers
from os import listdir
from newCleaner import get_root
import pickle, re
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

def get_alldiag(diag_xml_pathlst, metrics='coherence', flip=False):
    """metrics: the key in the diagnostics.xml attributes
    """
    cate = diag_xml_pathlst[0].split('/')[-3]
    print('Reading', cate, 'diagnostics...')
    if exists(CATE_COH_PKLPATH):
        with open(CATE_COH_PKLPATH) as cate_coh_dict:
            cate_diag = pickle.load(cate_coh_dict)
    else:
        cate_diag = dict()
        for xmlpath in diag_xml_pathlst:
            model_tpc_num, avg_mv = read_diag(xmlpath, metrics)
            if flip:
                avg_mv = -avg_mv
            cate_diag[model_tpc_num] = avg_mv
        # cate = basename(diag_xml_pathlst)
        if DUMPDICT:
            pickle.dump(cate_diag, join(results_path, cate+'_'+metrics[:4]+'.pkl'))
    if flip:
        metrics = metrics + ' (flipped)'
    return cate_diag, metrics, cate

# Perplexity
def get_perp(evaltxt_path):
    """Returns: dict with single item 
    key: num_of_topics; value: probability AFTER log transformation"""
    with open(evaltxt_path, 'r') as f:
        prob = float(f.read())
    # tpcnum = re.search(r'_(\d+)tpc', basename(evaltxt_path)).group(1)
    tpcnum = re.search(r'_(\d+)_heldoutprob',basename(evaltxt_path)).group(1)
    return tpcnum, prob

def get_allperp(eval_txt_pathlst):
    # cate = eval_txt_pathlst[0].split('/')[-3]
    cate = 'cs_t100'
    print('Reading', cate, 'perplexities...')
    perpdict = dict()
    for evaltxt in eval_txt_pathlst:
        tpcnum, prob = get_perp(evaltxt)
        perpdict[tpcnum] = -prob
    return perpdict, 'negative perplexity', cate

def plot_data(datadict, metrics, cate):
    x, y = zip(*datadict.items())
    x, y = np.array(x, dtype=int), np.array(y)
    idn = np.argsort(x)
    x, y = x[idn], y[idn]
    plt.plot(x, y, 'gs')
    
    mean, std = np.mean(y), np.std(y)
    horiz_line_data = np.array([mean for i in range(len(x))])
    plt.plot(x, horiz_line_data, 'r--') 
    plt.plot(x, np.array([mean+std for i in range(len(x))]), 'b--')
    plt.plot(x, np.array([mean-std for i in range(len(x))]), 'b--')
    # std: 255774.50041036308 ; mean: 255774.50041036308
    plt.xticks(x)
    plt.ylabel('Model '+metrics)
    # plt.xlabel('Num of topics')
    plt.xlabel('t100 model id')
    plt.title(cate.upper())
    # plt.axis([np.min(x), np.max(x), np.min(y), np.max(y)])
    plt.show()

def doublecurve(perpdict, diagdict, cate):
    plt.figure()
    for i, datadict in enumerate((perpdict, diagdict)):
        if i==0:
            plt.subplot(211)
            plt.ylabel('Negative perplexity')
        else:
            plt.subplot(212)
            plt.ylabel('Coherence')
        x, y = zip(*datadict.items())
        x, y = np.array(x, dtype=int), np.array(y)
        idn = np.argsort(x)
        x, y = x[idn], y[idn]
        plt.xticks(x)
        plt.plot(x, y)
    plt.xlabel('Num of topics')
   
    plt.suptitle(cate.upper())
    # plt.axis([np.min(x), np.max(x), np.min(y), np.max(y)])
    plt.show()

def doubleplot(datadict1, datadict2, metrics, cate):
    x, y = zip(*datadict1.items())
    x, y = np.array(x, dtype=int), np.array(y)
    idn = np.argsort(x)
    x, y = x[idn], y[idn]
    plt.plot(x, y, 'ro')

    x2, y2 = zip(*datadict2.items())
    x2, y2 = np.array(x2, dtype=int), np.array(y2)
    idn2 = np.argsort(x2)
    x2, y2 = x2[idn2], y2[idn2]
    plt.plot(x2, y2, 'bs')

    if len(x) > len(x2):
        plt.xticks(x)
    else:
        plt.xticks(x2)
    plt.ylabel('Model '+metrics)
    plt.xlabel('Num of topics')
    plt.title(cate.upper())
    # plt.axis([np.min(x), np.max(x), np.min(y), np.max(y)])
    plt.show()

if __name__ == "__main__":
    CATE_COH_PKLPATH = join(results_path, 'cs_coh.pkl')
    DUMPDICT = False
    
    # tpcnum_range = range(100,1001,50)
    tpcnum_range = [50,100]# range(5,101,5)
    modeldirx = '/cs/group/grp-glowacka/arxiv/models/cs_10k/model_'
    diag_xmls = [join(modeldirx+str(tpcnum), 'diagnostics.xml') for tpcnum in tpcnum_range]
    cohdict, cmt, cc = get_alldiag(diag_xmls, 'eff_num_words')
    # plot_data(cohdict, cmt, cc)

    # tpcnum_range = [100] # range(5,101,5)
    # testcompdirx = '/cs/group/grp-glowacka/arxiv/models/cs/cs_testcomp'
    # eval_txts = [join(testcompdirx, 'cs_heldout_'+str(tpcnum)+'tpc.txt') for tpcnum in tpcnum_range]
    # perpdict, pmt, pc = get_allperp(eval_txts)
    # print(perpdict)

    testcompdirx = '/cs/group/grp-glowacka/arxiv/models/cs_t100/cs_testcomp'
    eval_txts = [join(testcompdirx, txt) for txt in listdir(testcompdirx)]
    perpdict, pmt, pc = get_allperp(eval_txts)
    plot_data(perpdict, pmt, pc)
    # doubleplot(cohdict2, cohdict, pc)

    tpcnum_range = range(5,101,5)
    modeldirx = '/cs/group/grp-glowacka/arxiv/models/cs/model_'
    diag_xmls = [join(modeldirx+str(tpcnum), 'diagnostics.xml') for tpcnum in tpcnum_range]
    cohdict2, cmt2, cc2 = get_alldiag(diag_xmls, 'eff_num_words')
    
    tpcnum_range = [50,100]
    testcompdirx = '/cs/group/grp-glowacka/arxiv/models/cs_10k'
    eval_txts = [join(testcompdirx, 'cs_10kiter_heldout_'+str(tpcnum)+'tpc.txt') for tpcnum in tpcnum_range]
    perpdict2, pmt2, pc2 = get_allperp(eval_txts)

    # doubleplot(perpdict, perpdict2, pmt2, 'CS')
    
    # doubleplot(cohdict, cohdict2, cmt, 'CS')