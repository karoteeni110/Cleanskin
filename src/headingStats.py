import xml.etree.ElementTree as ET
import pickle
from os.path import join
from os import listdir
from newCleaner import get_root, is_section
from paths import results_path, cleanedxml_path
from collections import Counter

def get_headings(xmlpath):
    """Returns a dict. 
    keys: 'section', 'chapter'
    keys: list of section titles
    """
    _, root = get_root(xmlpath)
    secdict = {'section':[], 'chapter': []}
    for elem in root:
        if is_section(elem):
            secdict['section'].append(elem.get('title', '').lower())
        elif elem.tag == 'chapter':
            secdict['chapter'].append(elem.get('title', '').lower) 
            for subelem in elem:
                if is_section(elem):
                    secdict['section'].append(subelem.get('title', ''))
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
    print(count_headings(xmlpath_list).most_common(5))
    # [('introduction', 3480), ('', 2093), ('conclusions', 888), ('conclusion', 530), ('acknowledgments', 527)]
