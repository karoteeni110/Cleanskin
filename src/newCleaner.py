import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from metadata import get_urlid2meta
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
from collections import defaultdict
from unicodedata import normalize
import time, re

# Elements to be processed at level 1
# also: <section>, <ERROR>
keeplist = ['classification', 'keywords', 'para', 'backmatter', \
            'theorem', 'proof', 'appendix', 'bibliography', 'note', 'date', 'glossarydefinition', 'acknowledgements']
# Elements removed at all levels in the first place (EXCEPT 'ERROR')
# XXX: LV 1 <ERROR>s are not removed!!
removelist = ['cite', 'Math', 'figure', 'table', 'tabular', 'TOC', 'ERROR', 'pagination', 'rdf', 'index', \
        'toctitle', 'tags', 'tag', 'equation', 'equationgroup', 'ref', 'break', 'resource', 'indexmark', 'contact',\
            'abstract', 'creator']
sec_tags = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
sec_attribs = ['title', 'subtitle']
infer_errtags = {'abstract', 'address', 'affil', 'refb', 'reference', 'keywords', 'author', 'submitted'}
all_tags = keeplist + removelist + sec_tags + sec_attribs + ['abstract', 'author']

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

def remove_useless(root, tags = removelist):
    """Clear useless elements and keeps the trailing texts
    """
    # rmlist = []
    for tag in tags:
        if tag != 'ERROR':
            elems = root.findall('.//%s' % tag)
        else:
            elems = root.findall('./*//ERROR') # TODO: TEST IT
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
        if is_section(subelem):
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
    title = normalize('NFKD', ''.join(title.itertext())).lower().strip()
    return re.sub('\n', ' ', title)

def move_titles(root):
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

def is_fake_para(elem):
    if elem.tag == 'para':
        if elem.text.strip() in (metadata['author'], metadata['title'], metadata['abstract']):
            return True
    return False

def errtxt2tag(txt):
    if txt[0] == '\\':
        return txt[1:].lower()
    elif txt[0] == '{':
        return txt[1:-2].lower()
    else:
        return txt

def infer_err_abstract(docroot):
    """Infer {abstract, address, affil, } that are marked as <ERROR> & <para>s in the first level and retag the following <para>s
    """
    to_remove = []
    for i in range(0,len(docroot)-2):
        elempair = (docroot[i], docroot[i+1])
        # print(elempair[0].tag, elempair[1].tag)
        if elempair[0].tag == 'ERROR':
            to_remove.append(elempair[0])
            for t in infer_errtags:
                # print(t)
                if t in elempair[0].text.lower() and elempair[1].tag == 'para':
                    # to_remove.append(elempair[1])
                    
                    elempair[1].tag = t
                    print(elempair[1].tag, ''.join(elempair[1].itertext()))
            
    if docroot[-1].tag == 'ERROR':
        to_remove.append(docroot[-1])
    for error in to_remove:
        docroot.remove(error)

def remove_elems(toremovelst):
    for p, c in toremovelst:
        try:
            p.remove(c)
        except ValueError:
            continue

def clean(root):
    """Main function that cleans the XML.
    Keeps the subelements in section
    """
    toremove = []
    remove_useless(root)
    move_titles(root)
    infer_err_abstract(root)
    # print([elem.tag for elem in root])

    for rank1elem in root:  # 1st pass
        if rank1elem.tag in keeplist: # classification, keywords, ...
            flatten_elem(rank1elem)
            
            if is_empty_elem(rank1elem) or is_fake_para(rank1elem): # Remove empty paragraphs
                print('is empty or fake', rank1elem.tag)
                toremove.append((root,rank1elem))
                
        elif is_section(rank1elem) or is_chapter(rank1elem):
            retag_sec_or_chap(rank1elem)
            if rank1elem.get('title') == 'abstract':
                toremove.append((root, rank1elem))
            clean_sec(rank1elem)

        else:
            toremove.append((root, rank1elem)) # Don't modify it during iteration!
   
    remove_elems(toremove)
    
def is_empty_str(txt):
    if re.search(r'(\w|\d){5,}', txt) and \
        not re.match(r'^\W*fig(\.|ure)\W+\d+(\W+\(.*\))?\W*$' , txt, flags=re.I):
        return False
    return True

def is_empty_elem(elem):
    """True: elem.text does not contain any word or digit; elem.text contains only "figure XX"
    """
    try:
        txt = ''.join(elem.itertext())
        return is_empty_str(txt)
    except TypeError:
        print([chunk for chunk in elem.itertext()])
        return False

def have_inferable_sec(root):
    for elem in root:
        content = ''.join(elem.itertext())
        if re.match(r'introduction', content, flags=re.I) \
            and elem.tag != 'bibliography' \
            and elem.get('title', '').lower() != 'references':
            return True
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
    WRITE OUT the result to log
    MODIFIES root attribute `sec_state`: set to OK/full-text 
    """
    err = False
    errlog.write(xmlpath + ' \n')

    sections = root.findall('section') or root.findall('./chapter/section')

    if len(sections) == 0: # If abstract/section not found
        err = True
        # print(title + ' absent: ' + xmlpath)
        errlog.write('secs absent. ')
    
    # If sections exist but is empty
    for sec in sections:
        if is_empty_elem(sec):
            err = True
            # print('Empty ' + title + ' :' + xmlpath)
            errlog.write('Empty secs. ')
                                    
    if not err:
        errlog.write('OK. ')
        root.set('sec_state', 'OK')
    else:
        root.set('sec_state', 'full-text')
    
    if not root.get('abstract', False):
        errlog.write('Metadata not found. ')
    errlog.write('\n ================================== \n')


if __name__ == "__main__":
    # Set verbose
    VERBOSE, REPORT_EVERY = True, 100

    # Read metadata for all articles
    id2meta = get_urlid2meta() # 1 min

    # Set paths to dirty XMLs
    # xmlpath_list = [join(rawxmls_path, fn) for fn in listdir(rawxmls_path) if fn[-4:] == '.xml']
    xmlpath_list = [join(rawxmls_path, '=physics0002007.xml')]
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
            tree.write(join(cleanedxml_path, xml))
            # tree.write(join(results_path, xml))
            # tree.write(join(results_path, '1'+xml))

            if VERBOSE:
                if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmlpath_list):
                    print('%s of %s ...' % (i+1, len(xmlpath_list)))

    t = time.time() - begin
    t = t/60
    print(len(xmlpath_list), 'files in %s mins' % t)

    # With metadata:
    # 5163 files in 4.929596141974131 mins