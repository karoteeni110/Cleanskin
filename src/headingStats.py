import xml.etree.ElementTree as ET
import pickle, re
from os.path import join, basename
from os import listdir
from errortypes import subcate2cate
from newCleaner import get_root, is_section, is_empty_elem
from paths import results_path, cleanedxml_path
from collections import Counter
from unicodedata import normalize

def count_cates(xmlpath):
    _, root = get_root(xmlpath)
    subcates = root.get('categories', '').split(', ')
    cates = set(subcate2cate(subcate) for subcate in subcates)
    return len(cates)

def get_headings(xmlpath):
    """Returns a dict. 
    keys: 'section' (and 'chapter')
    values: list of section titles
    """
    _, root = get_root(xmlpath)
    secdict = {'section':[]}
    for k in secdict:
        for elem in root.findall('.//%s' % k):
            if not is_empty_elem(elem):
                secdict[k].append(elem.get('title', 'NO_TITLE'))
    # print(empty_sec_arts)
    return secdict

def count_headings(xmlpath_list):
    """Returns Counter([all_headings])
    """
    all_headings = []
    for i, xmlpath in enumerate(xmlpath_list):
        try:
            sec_titles = get_headings(xmlpath)['section']
            all_headings.extend(sec_titles)
        except ET.ParseError:
            print('Skipped: ParseError at %s' % xmlpath)
            continue
        
        if VERBOSE:
            if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmlpath_list):
                print('%s of %s ...' % (i+1, len(xmlpath_list)))
    return Counter(all_headings)

def show_cates_per_art():
    cter = Counter(str(count_cates(xml)) for xml in xmlpath_list)
    print(cter)
    for count in cter:
        print('%s articles associated with %s categories: %.4f ' % (cter[count], count, (cter[count]/sum(cter.values()))))

def show_seccount_per_art():
    sec_nums = []
    for xmlpath in xmlpath_list:
        sec_num = len(get_headings(xmlpath)['section'])
        sec_nums.append(str(sec_num))
    cter = Counter(sec_nums)
    print(cter)
    # non_zerosec_avg = sum(int(k)*cter[k] for k in cter if k != '0') / (sum(cter.values())-cter['0'])
    avg = sum(int(k)*cter[k] for k in cter) / sum(cter.values())
    print('Average: %s sections per article' % avg)

def show_sectitles_per_art():
    """
    """
    sectitle_cter = Counter()
    for xmlpath in xmlpath_list:
        sectitles = get_headings(xmlpath)['section']
        sectitle_cter.update([frozenset(sectitles)])
        if frozenset(sectitles) == frozenset({'introduction'}):
            print(xmlpath)
    for i in sectitle_cter.most_common(20):
        print(i)

def show(heading_freqlist):
    more_than_once = sum(freq for title,freq in heading_freqlist.most_common() if freq > 1)
    print('Total freq of titles that show more than once:', more_than_once)
    total_freq = sum(heading_freqlist.values())
    print('%.2f' % (more_than_once / total_freq), 'of', total_freq)

if __name__ == "__main__":
    VERBOSE, REPORT_EVERY = True, 100
    rootdir = cleanedxml_path
    xmlpath_list = [join(rootdir, xml) for xml in listdir(rootdir) if xml[-4:] == '.xml']
    # xmlpath_list = [join(cleanedxml_path, '=astro-ph0001424.xml')]
    heading_freqlist = count_headings(xmlpath_list) # length 12720

    print(len(heading_freqlist))
    # show(heading_freqlist)
    # [('introduction', 3510), ('conclusions', 893), ('conclusion', 541), ('acknowledgments', 528), ('discussion', 503), ('acknowledgements', 438), ('results', 343), ('summary', 257), ('concluding remarks', 123), ('preliminaries', 117), ('summary and conclusions', 92), ('appendix', 87), ('observations', 83), ('results and discussion', 80), ('discussion and conclusions', 79), ('acknowledgement', 73), ('numerical results', 65), ('the model', 65), ('proof of theorem', 60), ('acknowledgment', 59), ('references', 55), ('observations and data reduction', 55), ('summary and discussion', 54), ('', 45), ('related work', 39), ('examples', 38), ('applications', 35), ('introduction.', 32), ('model', 30), ('methods', 29), ('discussion and conclusion', 29), ('figure captions', 28)
    # Total sections: 22746
    # # of titles of which freq>1: 570
    # Total freq of titles that show more than once: 10605 (0.46623582168293326%)



    # show_cates_per_art()
    # Counter({'1': 4452, '2': 738, '3': 266, '4': 76, '5': 19, '6': 7, '7': 1})

    # show_seccount_per_art()
    # show_sectitles_per_art() # TODO: plot it!