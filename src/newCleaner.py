import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from metadata import get_urlid2meta
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
from unicodedata import normalize
import time, re

# Elements allowed at level 1
keeplist = ['subtitle', 'classification', 'keywords', 'para', 'backmatter', \
            'theorem', 'proof', 'appendix', 'bibliography', 'titlepage', 'note', 'date', 'glossarydefinition', 'acknowledgements']
# Elements removed in all levels in the first place
removelist = ['cite', 'Math', 'figure', 'table', 'tabular', 'TOC', 'ERROR', 'pagination', 'rdf', 'index', \
        'toctitle', 'tags', 'tag', 'equation', 'equationgroup', 'ref', 'break', 'resource', 'indexmark', 'contact',\
            'abstract', 'creator']
sec_tags = ['section', 'subsection', 'subsubsection', 'paragraph', 'subpragraph']
sec_attribs = ['title', 'subtitle']

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
        elems = root.findall('.//%s' % tag)
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
    txt = ''.join(elem.itertext())
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

def extract_abst(doc, titlepage):
    '''Extract abstract and move the element to within <document>
    USELESS: abstract is extract from metadata

    '''
    abstract = titlepage.find('abstract')
    if abstract:
        titlepage.remove(abstract)
        doc.insert(3,abstract)
        flatten_elem(abstract)

def retag_subsecs(parent_sec, child_sec):
    if 'section' in child_sec.tag:
        child_sec.tag = 'sub' + parent_sec.tag 

def retag_rank1secs(rank1elem):
    if is_section(rank1elem):
        rank1elem.tag = 'section'
        for subsec in rank1elem:
            retag_subsecs(rank1elem, subsec)
    elif is_chapter(rank1elem):
        rank1elem.tag = 'chapter'
        for elem in rank1elem:
            retag_rank1secs(elem)

def clean(root):
    """Main function that cleans the XML.
    Keeps the subelements in section
    """
    toremove = []
    remove_useless(root)
    move_titles(root)

    for rank1elem in root:  # 1st pass
        if rank1elem.tag in keeplist: # classification, keywords, ...
            flatten_elem(rank1elem)
            
            if is_empty_elem(rank1elem): # Remove empty paragraphs
                toremove.append((root,rank1elem))
                
        elif is_section(rank1elem) or is_chapter(rank1elem):
            retag_rank1secs(rank1elem)
            clean_sec(rank1elem)

        else:
            # print(rank1elem.tag) # <Float>
            toremove.append((root, rank1elem)) # Don't modify it during iteration!

    for p, c in toremove:
        try:
            p.remove(c)
        except ValueError:
            continue

def is_empty_str(txt):
    if re.search(r'(\w|\d)+', txt) and not re.match(r'^\W*fig(\.|ure)\W+\d+(\W+\(.*\))?\W*$' , txt, flags=re.I):
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
        if re.search(r'introduction', content, flags=re.I) \
            and elem.tag != 'bibliography' \
            and elem.get('title', '').lower() != 'references':
            return True
    return False

def fname2artid(fname):
    return fname.strip('=')[:-4] # strip ".xml"

def add_metamsg(docroot, fname):
    artid = fname2artid(fname)
    try:
        metadata = id2meta.pop(artid) # get retrive faster
    except KeyError as e:
        metadata = []
        print('Metadata not found:', e)
    docroot.attrib.clear()
    for attr in metadata:
        if attr == 'categories':
            docroot.set(attr, metadata[attr])
        else: # abstract, title, author
            subelem = ET.Element(attr)
            subelem.text = metadata[attr]
            # if attr == 'title':
            docroot.insert(0, subelem)
            # if attr == 'author':
            #     docroot.insert(1, subelem)
            # if attr == 'abstract':
            #     docroot.insert(2, subelem)

def postcheck(root, errlog):
    """Check if: 1) section is absent/empty; 2) metadata has been added to the root attrib
    WRITE OUT the result to log
    MODIFIES root attribute `sec_state`: set to OK/inferable/full-text 
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
    elif have_inferable_sec(root): # if there are paragraphs containing 'introduction'
        root.set('sec_state', 'inferable')
    else:
        root.set('sec_state', 'full-text')
    
    if not root.get('abstract', False):
        errlog.write('Metadata not found. ')
    errlog.write('\n ================================== \n')


if __name__ == "__main__":
    VERBOSE, REPORT_EVERY = True, 100
    xmlpath_list = [join(rawxmls_path, fn) for fn in listdir(rawxmls_path) if fn[-4:] == '.xml']
    # xmlpath_list = [join(rawxmls_path, '=astro-ph0001331.xml')]
    id2meta = get_urlid2meta() # 1 min

    begin = time.time()
    with open(cleanlog_path, 'w') as cleanlog:
        for i, xmlpath in enumerate(xmlpath_list):
            xml = basename(xmlpath)
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
            # tree.write(join(results_path, 'empty_sectitle.xml'))
            # tree.write(join(results_path, xml))

            if VERBOSE:
                if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmlpath_list):
                    print('%s of %s ...' % (i+1, len(xmlpath_list)))

    t = time.time() - begin
    t = t/60
    print(len(xmlpath_list), 'files in %s mins' % t)

    # With metadata:
    # 5163 files in 4.929596141974131 mins