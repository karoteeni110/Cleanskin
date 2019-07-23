from paths import cate_path, results_path, cleanlog_path
from os import listdir
from os.path import basename, join
from collections import defaultdict
import pickle 

cate2arts_path = join(results_path, 'cate2arts.pkl')
art2cates_path = join(results_path, 'arts2cate.pkl')
errtypes = {'OK', 'Empty abstract', 'Empty secs', 'secs absent', 'ParseError', 'abstract absent'}

def get_dicts(txtpath):
    cate2artsdict, art2catedict = defaultdict(set), defaultdict(set)
    with open(txtpath, 'r') as f:
        for line in f.readlines():
            artid, catelist = line.split()[0], line.split()[1].split(',')
            art2catedict[artid] = art2catedict[artid].union(set(catelist))
            for cate in catelist:
                cate2artsdict[cate].add(artid)
    return cate2artsdict, art2catedict

def merge_dicts(dict1, dict2):
    for k in dict2:
        if k in dict1:
            dict1[k] = dict1[k].union(dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1

def dump_dicts(cate2arts, art2cates):
    with open(cate2arts_path, 'wb') as d1:
        pickle.dump(cate2arts, d1)
    print('cate2arts -- dumped.')

    with open(art2cates_path, 'wb') as d2:
        pickle.dump(art2cates, d2)
    print('art2cates -- dumped.')

def get_pkls():
    cate2arts, art2cates = defaultdict(set), defaultdict(set)
    for txt in listdir(cate_path):
        print('Collecting: %s' % txt)
        txtpath = join(cate_path, txt)
        c2a, a2c = get_dicts(txtpath)
        cate2arts, art2cates = merge_dicts(cate2arts, c2a), merge_dicts(art2cates, a2c)
    # print(cate2arts['astro-ph'])
    dump_dicts(cate2arts, art2cates)

def read_pkls():
    return pickle.load(open(cate2arts_path,'rb')), pickle.load(open(art2cates_path, 'rb'))

def pe_generator(f):
    artid = basename(f.readline()[:-2])[:-4].strip('=')
    errmsgs = f.readline()[:-1].split('. ')[:-1] # get rid of \n
    _ = f.readline()
    return (artid, errmsgs)

def read_xmlcleaner_log():
    '''
    Returns ``cleaner_results`` : a list of (artID, errmsgs)
    '''
    with open(cleanlog_path, 'r') as log:
        cleaner_results = []
        pe_pair = pe_generator(log)
        while '' not in pe_pair: # loop until it reaches the end of the file
            cleaner_results.append(pe_pair)
            pe_pair = pe_generator(log)
    return cleaner_results

def count_case(cleaner_results, errtype):
    '''
    Error types: {'Empty abstract', 'Empty secs', 'OK', 'secs absent', 'ParseError', 'abstract absent'}
    '''
    # return set(i for _, msg in cleaner_results for i in msg) 
    return sum(1 for _, errmsg in cleaner_results if errtype in errmsg)

def show_errtype_stats():
    cleaner_results = read_xmlcleaner_log()
    print(len(cleaner_results), 'xmls in all')
    print()
    for err in errtypes:
        print(err, count_case(cleaner_results, err))

    # Empty secs 453
    # abstract absent 1167
    # secs absent 1110
    # OK 3151
    # Empty abstract 44
    # ParseError 16

def id2dictkey(artid):
    # TODO
    return artid

def count_errcates():
    cleaner_results = read_xmlcleaner_log()
    err_counter = {}

    # Initialize the counter for each error type
    for errtype in errtypes: 
        err_counter[errtype] = defaultdict(int)
    
    # Traverse articles
    for artid, errs in cleaner_results:
        # TODO: convert ``artid`` into recognizable format for ``art2cates`` 
        cates = art2cates[id2dictkey(artid)]
        for err in errs:
            for cate in cates:
                err_counter[err][cate] += 1
    return err_counter

def show_err_distrib():
    distrib = count_errcates()
    for err in distrib:
        if err != 'OK':
            print(err+':')
            for cate in distrib[err]:
                count = distrib[err][cate]
                # if count > 1:
                print(cate, count)
            print()

if __name__ == "__main__":
    cate2arts, art2cates = read_pkls()
    clean_results = read_xmlcleaner_log()
    # show_errtype_stats()
    show_err_distrib()


