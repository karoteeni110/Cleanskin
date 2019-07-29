from paths import cate_path, results_path, cleanlog_path
from os import listdir
from os.path import basename, join
from collections import defaultdict
from newCleaner import get_root, normalize_txt
import pickle 

cate2arts_path = join(results_path, 'cate2arts.pkl')
art2cates_path = join(results_path, 'arts2cate.pkl')
err2arts_path = join(results_path, 'err2arts.pkl')
ERRTYPES = {'OK', 'Empty abstract', 'Empty secs', 'secs absent', 'ParseError', 'abstract absent'}

def get_dicts(txtpath):
    cate2artsdict, art2catedict = defaultdict(set), defaultdict(set)
    with open(txtpath, 'r') as f:
        for line in f.readlines():
            artid, catelist = line.split()[0], [cate.split('.')[0] for cate in line.split()[1].split(',')] # Remove subclass
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
    # print(categet_ph'])
    dump_dicts(cget_2cates)

def read_pkls():get_
    a, b, c = open(cate2arts_path,'rb'), open(art2cates_path, 'rb'), open(err2arts_path, 'rb')
    d1, d2, d3 = pickle.load(a), pickle.load(b), pickle.load(c)
    a.close()
    b.close()
    c.close()
    return d1, d2, d3

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

def get_err2arts_dict():
    cleaner_results = read_xmlcleaner_log()
    d = defaultdict(set)
    for artid, errmsgs in cleaner_results:
        for err in errmsgs:
            d[err].add(artid)
    return d

def count_case(cleaner_results, errtype):
    '''
    Error types: {'OK', 'Empty abstract', 'Empty secs', 'secs absent', 'ParseError', 'abstract absent', 'External paras'}

    '''
    # return set(i for _, msg in cleaner_results for i in msg) 
    return sum(1 for _, errmsg in cleaner_results if errtype in errmsg)

def show_errtype_stats(errtypes=ERRTYPES):
    cleaner_results = read_xmlcleaner_log()
    print(len(cleaner_results), 'xmls in all')
    print()
    for err in errtypes:
        print(err, count_case(cleaner_results, err))

def fn2dictkey(artid):
    # TODO
    return artid

def count_errcates():
    cleaner_results = read_xmlcleaner_log()
    err_counter = {}

    # Initialize the counter for each error type
    for errtype in ERRTYPES: 
        err_counter[errtype] = defaultdict(int)
    
    # Traverse articles
    for artid, errs in cleaner_results:
        # TODO: convert ``artid`` into recognizable format for ``art2cates`` 
        cates = art2cates[fn2dictkey(artid)]
        for err in errs:
            for cate in cates:
                err_counter[err][cate] += 1
    return err_counter

def show_errtype_cates(errtypes=ERRTYPES):
    distrib = count_errcates()
    for err in errtypes:
        if err != 'OK':
            print(err+':')
            errlst = []
            for cate in distrib[err]:
                errlst.append((cate, distrib[err][cate]))
                # if count > 1:
            print(sorted(errlst, key=lambda x:x[1]))
            print()

def show_errtype_arts(errtypes=ERRTYPES):
    err2arts = get_err2arts_dict()
    for err in errtypes:
        if err != 'OK':
            print(err+':')
            print(err2arts[err])
            print()

def is_title(elem):
    pass

def have_title(xmlpath):
    _, root = get_root(xmlpath)
    for elem in root:
        content = ''.join(elem.itertext())
        if 'introduction' in normalize_txt(content):
            return True
    return False

def show_false_neg():
    all_nosec = get_err2arts_dict()['secs absent']
    false_nosec = ''
    print('Detected titles: %s in %s' % (len(false_nosec), len(all_nosec)))
    print()

if __name__ == "__main__":
    clean_results = read_xmlcleaner_log()
    show_errtype_arts(['secs absent'])
    # show_errtype_stats()
    # show_errtype_cates(['Empty abstract'])


    # 5575 xmls in all

    # ParseError 16
    # Empty abstract 44
    # Empty secs 453
    # secs absent 1110
    # OK 1906
    # abstract absent 1167


    # anotherCleaner.py
    # 5575 xmls in all

    # ParseError 16
    # secs absent 1109
    # abstract absent 1013
    # Empty abstract 44
    # OK 3273
    # Empty secs 455
