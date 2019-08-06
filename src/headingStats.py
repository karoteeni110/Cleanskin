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

def show_heading_stats():
    heading_cter = count_headings(xmlpath_list)

if __name__ == "__main__":
    VERBOSE, REPORT_EVERY = True, 100
    rootdir = cleanedxml_path
    xmlpath_list = [join(rootdir, xml) for xml in listdir(rootdir) if xml[-4:] == '.xml']
    # xmlpath_list = ['/home/local/yzan/Desktop/Cleanskin/results/cleaned_xml/=astro-ph0001424.xml']
    print(count_headings(xmlpath_list).most_common(80))
    # [('introduction', 3510), ('conclusions', 893), ('conclusion', 541), ('acknowledgments', 528), ('discussion', 503), ('acknowledgements', 438), ('results', 343), ('summary', 257), ('concluding remarks', 123), ('preliminaries', 117), ('summary and conclusions', 92), ('appendix', 87), ('observations', 83), ('results and discussion', 80), ('discussion and conclusions', 79), ('acknowledgement', 73), ('numerical results', 65), ('the model', 65), ('proof of theorem', 60), ('acknowledgment', 59), ('references', 55), ('observations and data reduction', 55), ('summary and discussion', 54), ('', 45), ('related work', 39), ('examples', 38), ('applications', 35), ('introduction.', 32), ('model', 30), ('methods', 29), ('discussion and conclusion', 29), ('figure captions', 28)