import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path, no_sec_xml, cleaned_nonsecs
from metadata import get_urlid2meta
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
from collections import defaultdict
from unicodedata import normalize
import time, re

# Elements directly flattened at level 1
# Modification for <para> <section> and <ERROR> are different
keeplist = ['classification', 'keywords', 'backmatter', 'glossarydefinition', 'acknowledgements',\
            'theorem', 'proof', 'appendix', 'bibliography', 'date']
# Elements removed at all levels in the first place (EXCEPT 'ERROR')
# XXX: LV 1 <ERROR>s are NOT removed!!
removelist = ['ERROR','cite', 'Math', 'figure', 'table', 'tabular', 'TOC', 'pagination', 'rdf', 'index', \
        'toctitle', 'tags', 'tag', 'equation', 'equationgroup', 'ref', 'break', 'resource', 'indexmark', 'contact',\
            'abstract', 'creator', 'titlepage', 'note', 'graphics']
inferables = ['para', 'ERROR']
sec_tags = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
sec_attribs = ['title', 'subtitle']
infer_errtags = {'abstract', 'address', 'affil', 'refb', 'reference', 'keywords', 'author', 'submitted'}
all_tags = keeplist + removelist + sec_tags + sec_attribs + inferables + ['abstract', 'author'] 
nonsec_titles = ['acknowledgements', 'acknowledgement', 'acknowledgment', 'acknowledgments', 'references', 'figure captions']

remove_num_pt= r'((?!i+\W|vi{0,4}\W|iv\W)\b[a-z]+(\s)?)+'

def ignore_ns(root):
    '''Clean namespace in the node's tag. Should be called in the first place.
    '''
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

def get_root(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    ignore_ns(root)
    return tree, root

def retag_useless(root, tags = removelist):
    """Clear useless elements, move .tail to .text
    Empty elements would either be flattened if depth > 1 or be removed by func `clean()` 
    """
    # rmlist = []
    for tag in tags:
        if tag != 'ERROR':
            elems = root.findall('.//%s' % tag)
        else:
            elems = root.findall('./*//ERROR')
        for elem in elems: 
            txt = elem.tail
            elem.clear()
            elem.tag = 'throwit'
            elem.text = txt
        

def clean_attribs(elem, oldatts):
    elem.attrib.clear()
    for useful_attr in sec_attribs:
        if oldatts.get(useful_attr) != None:
            elem.set(useful_attr, oldatts[useful_attr])

def remove_margin(txt):
    return re.sub(r'(\[\d+(mm|ex|cm|pt)\])', '', txt)

def flatten_elem(elem):
    """Remove all the subelements; keep only text and useful attributes
    """
    oldatts = elem.attrib
    txt = ' '.join(t.strip() for t in elem.itertext())
    elem.clear()
    clean_attribs(elem, oldatts)
    elem.text = remove_margin(txt)

def is_chapter(elem):
    if elem.tag in ('chapter', 'part') and have_subsec(elem):
        return True
    return False

def is_section(elem):
    if elem.tag in sec_tags:
        return True
    elif elem.tag in ('chapter', 'part') and not have_subsec(elem) and have_title(elem):
        return True
    return False    

def clean_sec(sec):
    """Flatten subelements that are not <subsection>; rename <bibitem> to <bibliography>;
    remove empty subelements; clear all attributes except <title>
    """
    to_removes = []
    for subelem in sec:
        if subelem.tag == 'bibitem':
            subelem.tag = 'bibliography'
        elif is_section(subelem):
            clean_sec(subelem)
        else:
            flatten_elem(subelem)

            if is_empty_elem(subelem):
                to_removes.append(subelem)
    for to_remove in to_removes:
        sec.remove(to_remove)
    oldatts = sec.attrib.copy()
    clean_attribs(sec, oldatts)

def have_title(elem):
    return elem.get('title', False)

def have_subsec(elem):
    for subelem in elem:
        if is_section(subelem):
            return True
    return False

def normalize_title(title):
    """Remove Unicode chars & new lines in the title element `title`
    """
    normed_title = normalize('NFKD', ''.join(title.itertext())).strip() # remove unicode chars, strip spaces
    normed_title = re.sub('\n', ' ', normed_title) # space in place of new lines
    
    # == Remove numerals before title
    ttmatch = re.search(remove_num_pt, normed_title, flags=re.I) 
    if ttmatch != None:
        normed_title = ttmatch.group(0)
    # ==
    
    if normed_title.isspace():
        normed_title = ''
    return normed_title

def mv_titles(root):
    """Set all the <title>s as the parent node's attribute and remove it from the parent.
    Should be called first.
    """
    to_remove = []
    for title_parent in root.findall('.//title/..'):
        title, subtitle = title_parent.find('title'), title_parent.find('subtitle')
        for t in [title, subtitle]:
            if t != None and title_parent.tag != 'document':
                to_remove.append((title_parent, t))
                title_content = normalize_title(t)
                if title_parent.tag in ('theorem', 'proof') and is_empty_str(title_content):
                    continue
                else:
                    title_parent.set(t.tag, title_content)
    for p,c in to_remove:
        p.remove(c)

def retag_subsecs(parent_sec, childelem):
    if 'section' in childelem.tag:
        childelem.tag = 'sub' + parent_sec.tag 
    elif 'paragraph' in childelem.tag:
        childelem.tag = 'paragraph'
    # Retag subsubparagraphs recursively
    for para_or_subpara in childelem:
        retag_subsecs(childelem, para_or_subpara)

def retag_sec_or_chap(rank1elem):
    if is_section(rank1elem):
        rank1elem.tag = 'section'
        for para_or_subsec in rank1elem:
            retag_subsecs(rank1elem, para_or_subsec)
    elif is_chapter(rank1elem):
        rank1elem.tag = 'chapter'
        for elem in rank1elem:
            retag_sec_or_chap(elem)

def infer_errelem(elem_err, following_elem):
    """Pick rank-1 <ERROR> that contains `infer_errtags` 
    and retag its following <para>s
    """
    if following_elem.tag == 'para':
        for t in infer_errtags:
            if t in elem_err.text.lower(): # if text contains keywords
                following_elem.tag = t
                # print(elempair[1].tag, ''.join(elempair[1].itertext()))

def remove_elems(toremovelst):
    for p, c in toremovelst:
        try:
            p.remove(c)
        except ValueError:
            continue

def next_elem(current_idx, parent):
    if current_idx == len(parent)-1:
        return None
    else:
        return parent[current_idx+1]

def normed_str(txt):
    if type(txt) == str:
        t = txt
    elif txt == None:
        t = ''
    normed = normalize('NFKD', t).strip()
    if is_empty_str(normed):
        normed = None
    return normed

def get_next_para(present_para, docroot):
    present_para_idx = list(docroot).index(present_para)
    idx = present_para_idx+1
    while docroot[idx].tag != 'para' and idx < len(docroot):
        idx+=1
    if docroot[idx].tag == 'para':
        return docroot[idx]

def rm_inferred_ab(docroot):
    paras = docroot.findall("./para/p[1]/text[1]/../..")

    for para in paras:
        elem_p = para.find('p') # first <p>
        if elem_p:
            elem_text = elem_p.find('text') # first <text>

            elem_text.text = normed_str(elem_text.text)
            elem_text.tail = normed_str(elem_text.tail)

            if elem_text.text:
                if elem_p.text == None and re.match('abstract', elem_text.text, flags=re.I):
                    if len(normed_str(''.join(elem_p.itertext()))) <= 10:
                        p_idx = 0
                        while para[p_idx].tag != 'p':
                            p_idx += 1
                        try:
                            para[p_idx+1].clear()
                        except IndexError:
                            nextpara = get_next_para(para, docroot)
                            if nextpara:
                                nextpara.clear()
                    elem_p.clear()

def infer_sectitles(root):
    paras = root.findall("./para/p[1]/text[1]/../..")
    for para in paras:
            elem_p = para.find('p')
            elem_text = elem_p.find('text') 

            elem_text.text = normed_str(elem_text.text)
            elem_text.tail = normed_str(elem_text.tail)

            if elem_text.text:
                # cintropt = r'((\W)?(1|0|i+|vi{0,4}|iv)?(\W)*?introduction)'
                if elem_p.text == None: #and re.match(intropt, elem_text.text, flags=re.I):
                    # if len(normed_str(''.join(elem_p.itertext()))) >= 15:
                    if len(elem_text.text.split()) <= 8 and len(para.findall('p'))==1:
                        elem_text.text = None
                        elem_text.attrib.clear()
                        elem_p.tag = 'para'
                        elem_p.attrib.clear()
                        flatten_elem(elem_p)
                        para.tag = 'section'
                        para.attrib.clear()
                        para.set('title', 'Introduction')

                        
def infersecs(root):
    infer_sectitles(root)
    # reshape_paras(root)


def clean(root):
    """Remove all the subelements that are not 
    Keeps the subelements in section
    """
    toremove = []
    # ===== DFS operations: =====
    retag_useless(root)
    mv_titles(root)
    
    # infer_err_abstract(root)

    for rank1elem in root:
        if is_section(rank1elem) or is_chapter(rank1elem):
            retag_sec_or_chap(rank1elem)

    if root.find('abstract') is None:
        rm_inferred_ab(root)
    
    if root.find('section') is None:
        infersecs(root)
        root.set('sec_state', 'inferred')


    # ===== BFS operations: =====
    for i, rank1elem in enumerate(root):  # 1st pass

        # ===== Single elements process, no inference needed: =====
        if rank1elem.tag in keeplist: # classification, keywords, ...
            flatten_elem(rank1elem)
            
        elif rank1elem.tag in ('section', 'chapter'):
            if rank1elem.get('title') == 'abstract':
                toremove.append((root, rank1elem))
            clean_sec(rank1elem)

        # ===== Pair of elements process, if `rank1elem.tag` in `inferables`: =====
        elif rank1elem.tag == 'ERROR':
            toremove.append((root, rank1elem))
            if next_elem(i, root):
                infer_errelem(rank1elem, next_elem(i, root))
        
        elif rank1elem.tag == 'para':
            flatten_elem(rank1elem)

        else:
            toremove.append((root, rank1elem)) # NO modifying during iteration!

        if is_empty_elem(rank1elem):
            toremove.append((root, rank1elem))
   
    remove_elems(toremove)
    
def is_empty_str(txt):
    if txt.isspace(): # contains only space
        return True 
    elif re.search(r'[a-zA-Z]+?', txt) == None: # does not have words
        return True
    elif re.match(r'^\W*fig(\.|ure)\W+\d+(\W+\(.*\))?\W*$' , txt, flags=re.I):
        return True
    return False

def is_empty_elem(elem):
    """True: elem.text does not contain any word or digit; elem.text contains only "figure XX"
    """
    try:
        txt = ''.join(elem.itertext())
        # if not is_empty_str(txt) and elem.tag == 'p':
        #     print(txt)
        return is_empty_str(txt)
    except TypeError:
        print([chunk for chunk in elem.itertext()])
        return False

def fname2artid(fname):
    return fname.strip('=')[:-4] # strip ".xml"

def add_metamsg(docroot, fname):
    docroot.attrib.clear()
    for attr in metadata:
        if attr == 'categories':
            docroot.set(attr, metadata[attr])
        else: # abstract, title, author
            subelem = ET.Element(attr)
            subelem.text = metadata[attr]
            docroot.insert(0, subelem)

def postcheck(root, errlog):
    """Check if: 1) section is absent/empty; 2) metadata has been added to the root attrib
    WRITE OUT the result to log: 
            0: section OK
            1: no sections
            2: empty sections
            3: metadata not found
    MODIFIES root attribute `sec_state`: set to OK/full-text 
    """
    err = False
    errlog.write(xmlpath + ' \n')

    if root.find('section') is None: # If abstract/section not found OR section is acknowledgement/figure caption/references
        err = True
        # print(title + ' absent: ' + xmlpath)
        errlog.write('1') # No sections
    
    # If sections exist but is empty

    elif root.find('section') is False:
        err = True
        # print('Empty ' + title + ' :' + xmlpath)
        errlog.write('2') # Empty sections
                                    
    if not err and not root.get('sec_state', False):
        errlog.write('0')
        root.set('sec_state', 'OK')
    else:
        root.set('sec_state', 'full-text')
    
    if not root.get('abstract', False):
        errlog.write('3') # Metadata not found
    errlog.write('\n ================================== \n')


if __name__ == "__main__":
    # Set verbose
    VERBOSE, REPORT_EVERY = True, 100

    # Read metadata for all articles
    id2meta = get_urlid2meta() # 1 min

    # Set paths to dirty XMLs
    # xmlpath_list = [join(rawxmls_path, fn) for fn in listdir(rawxmls_path) if fn[-3:] == 'xml']
    xmlpath_list = [join(no_sec_xml, fn) for fn in listdir(no_sec_xml) if fn[-3:] == 'xml']
    # xmlpath_list = [join(rawxmls_path, '=physics0002007.xml')]
    # xmlpath_list = [join(results_path, 'test.xml')]

    # Cleaning
    begin = time.time()
    with open(cleanlog_path, 'w') as cleanlog:
        for i, xmlpath in enumerate(xmlpath_list):
            xml = basename(xmlpath)

            # === Get title, author, abstract, categories from metadata ===
            artid = fname2artid(xml)
            try:
                metadata = id2meta.pop(artid) # get retrive faster
            except KeyError as e:
                metadata = defaultdict(str)
                print('Metadata not found:', e)
            # === 

            try:
                tree, root = get_root(xmlpath)
            except ET.ParseError:
                print('Skipped: ParseError at %s' % xmlpath)
                cleanlog.write(xmlpath + ' \n' + 'ParseError. \n' + '================================== \n')
                continue
            clean(root)
            add_metamsg(root, xml)
            postcheck(root, cleanlog)
            # tree.write(join(cleanedxml_path, xml))
            # tree.write(join(results_path, xml))
            tree.write(join(cleaned_nonsecs, xml))

            if VERBOSE:
                if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmlpath_list):
                    print('%s of %s ...' % (i+1, len(xmlpath_list)))

    t = time.time() - begin
    t = t/60
    print(len(xmlpath_list), 'files in %s mins' % t)

    # With metadata:
    # 5163 files in 5.088259251912435 mins