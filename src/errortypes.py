from os import listdir
from os.path import basename, join, exists, dirname
from collections import defaultdict, Counter
from shutil import copyfile, copytree
from useLatexml import pick_toptex
from newCleaner import ignore_ns
from paths import *
import pickle, re
import xml.etree.ElementTree as ET

cate2arts_path = join(results_path, 'cate2arts.pkl')
art2cates_path = join(results_path, 'arts2cate.pkl')
err2arts_path = join(results_path, 'err2arts.pkl')
ERRTYPES = {'OK', 'Empty secs', 'secs absent', 'ParseError', 'Metadata not found'} # , 'Empty abstract','abstract absent'}

def normalize_txt(txt):
    return normalize('NFKD', txt).lower().strip()

def get_root(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    ignore_ns(root)
    return tree, root

def subcate2cate(subcate):
    return subcate.split('.')[0]

def get_dicts(txtpath):
    cate2artsdict, art2catedict = defaultdict(set), defaultdict(set)
    with open(txtpath, 'r') as f:
        for line in f.readlines():
            artid = line.split()[0].replace('/','')
            catelist = [subcate2cate(subcate) for subcate in line.split()[1].split(',')] # Remove subclass
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

def get_latest_pkls():
    cate2arts, art2cates = defaultdict(set), defaultdict(set)
    for txt in listdir(cate_path):
        print('Collecting: %s' % txt)
        txtpath = join(cate_path, txt)
        c2a, a2c = get_dicts(txtpath)
        cate2arts, art2cates = merge_dicts(cate2arts, c2a), merge_dicts(art2cates, a2c)
    dump_dicts(cate2arts, art2cates)

def read_pkls():
    a, b, c = open(cate2arts_path,'rb'), open(art2cates_path, 'rb'), open(err2arts_path, 'rb')
    cate2arts, art2cates, err2arts = pickle.load(a), pickle.load(b), pickle.load(c)
    a.close()
    b.close()
    c.close()
    return cate2arts, art2cates, err2arts

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

# def fn2dictkey(artid):
#     # TODO
#     return artid

def count_errcates():
    cleaner_results = read_xmlcleaner_log()
    err_counter = {}

    # Initialize the counter for each error type
    for errtype in ERRTYPES: 
        err_counter[errtype] = defaultdict(int)
    
    # Traverse articles
    for artid, errs in cleaner_results:
        cates = art2cates[artid]
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

def have_intro_in_xml(xmlpath):
    _, root = get_root(xmlpath)
    for elem in root:
        content = ''.join(elem.itertext())
        if 'introduction' in content.lower() and elem.tag != 'bibliography' and elem.get('title', '').lower() != 'references':
            return True
    return False

def have_sec_in_latex(latexpath):
    with open(latexpath, 'r', encoding='utf-8', errors='ignore') as f:
        tex = f.read()
        if re.search(r'introduction', tex, flags=re.I):
            return True
        else:
            return False

def art2latexpath(art):
    if '1701' in art:
        artpath = join(data1701, '='+art)
    elif '0001' in art:
        artpath = join(data0001, '='+art)
    elif '0002' in art:
        artpath = join(data0002, '='+art)
    return join(artpath, pick_toptex(artpath))

def art2latexdirpath(art):
    return dirname(art2latexpath(art))

def art2dirtyxmlpath(art):
    return join(rawxmls_path, '=' + art + '.xml')

def art2cleanxmlpath(art):
    return join(cleanedxml_path, '=' + art + '.xml')

def show_false_neg():
    all_nosec = get_err2arts_dict()['secs absent']
    false_nosec = []
    for art in all_nosec:
        # path = art2latexpath(art) 
        path = art2cleanxmlpath(art)
        
        if exists(path):
            if True: # not have_sec_in_latex(path):
                # print(path)
                # continue

                false_nosec.append(art)
        else:
            print('not found:', art)
    print('Detected titles: %s in %s' % (len(false_nosec), len(all_nosec)))

    s = []
    for i in false_nosec:
        cate = art2cates[i]
        s.extend(cate)
    ct = Counter(s)
    print(ct.most_common(50))
    # print(sum(n for t, n in ct.most_common(50)))
    # Articles where 'introdution' is not detected: 
    # Detected titles: 732 in 1109
    # [('cond-mat', 331), ('hep-ph', 139), ('hep-th', 71), ('quant-ph', 70), ('astro-ph', 59), ('math', 52), ('physics', 47), ('gr-qc', 43), ('nucl-th', 39), ('hep-ex', 34), 
    # ('nlin', 21), ('math-ph', 19), ('nucl-ex', 17), ('hep-lat', 15), ('cs', 8), ('q-bio', 5), ('stat', 2), ('q-fin', 1)]
    
    # Detected no titles: 843 in 1109
    # [('cond-mat', 398), ('hep-ph', 153), ('hep-th', 92), ('quant-ph', 83), ('math', 61), ('astro-ph', 59), ('physics', 53), ('gr-qc', 46), ('nucl-th', 39), ('hep-ex', 37), 
    # ('nlin', 23), ('math-ph', 23), ('hep-lat', 18), ('nucl-ex', 18), ('cs', 10), ('q-bio', 6), ('q-fin', 4), ('stat', 2)]
        
def cp_errtypefiles(errtype, destdirpath):
    all_errfiles = get_err2arts_dict()[errtype]
    for art in all_errfiles:
        path = art2dirtyxmlpath(art)
        if exists(path):
            try:
                copyfile(path, join(destdirpath, basename(path)))
            except FileExistsError as e:
                print(e)
                continue


if __name__ == "__main__":
    # get_latest_pkls()
    cate2arts, art2cates, err2arts = read_pkls()
    clean_results = read_xmlcleaner_log()
    # print(cate2arts['hep-th'])
    # show_errtype_arts(['secs absent'])
    # show_false_neg()
    # cp_errtypefiles('secs absent', destdirpath=no_sec_xml)
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
