import xml.etree.ElementTree as ET
import pickle
from os.path import join, basename
from os import listdir
from errortypes import subcate2cate
from newCleaner import get_root, is_section, is_empty
from paths import results_path, cleanedxml_path
from collections import Counter
from unicodedata import normalize

def get_title(elem):
    title = normalize('NFKD', elem.get('title', '')).lower().strip()
    return title 

def count_cates(xmlpath):
    _, root = get_root(xmlpath)
    subcates = root.get('categories', '').split(', ')
    cates = set(subcate2cate(subcate) for subcate in subcates)
    return len(cates)

def get_headings(xmlpath):
    """Returns a dict. 
    keys: 'section', 'chapter'
    values: list of section titles
    """
    _, root = get_root(xmlpath)
    secdict = {'section':[], 'chapter': []}
    empty_sec_arts = set()
    for elem in root:
        if is_section(elem) and not is_empty(elem):
            if get_title(elem) == '':
                empty_sec_arts.add(basename(xmlpath))

            secdict['section'].append(get_title(elem))
        elif elem.tag == 'chapter':
            secdict['chapter'].append(get_title(elem)) 
            for subelem in elem:
                if is_section(subelem) and not is_empty(subelem):
                    secdict['section'].append(get_title(subelem))
    # print(empty_sec_arts)
    return secdict

def count_headings(xmlpath_list):
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
    cter = Counter(all_headings)
    return cter

def show_cates_per_art():
    cter = Counter(str(count_cates(xml)) for xml in xmlpath_list)
    print(cter)
    for count in cter:
        print('%s articles associated with %s categories: %.4f ' % (cter[count], count, (cter[count]/sum(cter.values()))))

def show_sec_per_art():
    sec_nums = []
    for xmlpath in xmlpath_list:
        sec_num = len(get_headings(xmlpath)['section'])
        sec_nums.append(str(sec_num))
    cter = Counter(sec_nums)
    print(cter)
    print('Not 0:', sum(cter.values())-cter['0'])


if __name__ == "__main__":
    VERBOSE, REPORT_EVERY = True, 100
    rootdir = cleanedxml_path
    xmlpath_list = [join(rootdir, xml) for xml in listdir(rootdir) if xml[-4:] == '.xml']
    # xmlpath_list = [join(cleanedxml_path, '=astro-ph0001424.xml')]

    # print(count_headings(xmlpath_list).most_common(500))
    # [('introduction', 3510), ('conclusions', 893), ('conclusion', 541), ('acknowledgments', 528), ('discussion', 503), ('acknowledgements', 438), ('results', 343), ('summary', 257), ('concluding remarks', 123), ('preliminaries', 117), ('summary and conclusions', 92), ('appendix', 87), ('observations', 83), ('results and discussion', 80), ('discussion and conclusions', 79), ('acknowledgement', 73), ('numerical results', 65), ('the model', 65), ('proof of theorem', 60), ('acknowledgment', 59), ('references', 55), ('observations and data reduction', 55), ('summary and discussion', 54), ('', 45), ('related work', 39), ('examples', 38), ('applications', 35), ('introduction.', 32), ('model', 30), ('methods', 29), ('discussion and conclusion', 29), ('figure captions', 28)
    
    # show_cates_per_art()
    # Counter({'1': 4452, '2': 738, '3': 266, '4': 76, '5': 19, '6': 7, '7': 1})
    # 4452 articles associated with 1 categories: 0.8009 
    # 738 articles associated with 2 categories: 0.1328 
    # 76 articles associated with 4 categories: 0.0137 
    # 266 articles associated with 3 categories: 0.0479 
    # 19 articles associated with 5 categories: 0.0034 
    # 7 articles associated with 6 categories: 0.0013 
    # 1 articles associated with 7 categories: 0.0002

    show_sec_per_art()