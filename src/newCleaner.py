import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from abstractFromMeta import add_abstract
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
from unicodedata import normalize
import time


keeplist = ['title', 'subtitle', 'classification', 'abstract', 'creator', 'keywords', 'para', \
            'theorem', 'proof', 'appendix', 'bibliography', 'titlepage', 'note', 'date', 'glossarydefinition']
sec_tags = ['section', 'subsection', 'subsubsection', 'paragraph', 'subpragraph']
useful_attribs = ['title', 'subtitle']

def ignore_ns(root):
    '''
    Clean namespace in the node's tag. Should be called in the first place.
    '''
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

def remove_useless(root, tags = ['cite', 'Math', 'figure', 'table', 'TOC', 'ERROR', 'pagination', 'rdf', 'index', \
                    'toctitle', 'tags', 'tag', 'equation', 'equationgroup', 'ref', 'break', 'resource', 'indexmark']):
    """Remove useless elements with keeping the trailing texts
    """
    # rmlist = []
    for tag in tags:
        elems = root.findall('.//%s' % tag)
        for elem in elems: 
            txt = elem.tail
            elem.clear()
            elem.tag = 'p'
            elem.text = txt

def flatten_elem(elem):
    oldatt = elem.attrib
    txt = ''.join(elem.itertext())
    elem.clear()
    for useful_attrib in useful_attribs:
        if oldatt.get(useful_attrib, None):
            elem.set(useful_attrib, oldatt[useful_attrib])
    elem.text = txt

def is_section(elem):
    if elem.tag in sec_tags or have_subsec(elem):
        return True
    else:
        return False    

def clean_sec(sec):
    for subelem in sec:
        if is_section(subelem):
            clean_sec(subelem)
        else:
            flatten_elem(subelem)

def have_title(elem):
    return elem.get('title', False)

def have_subsec(elem):
    for subelem in elem:
        if is_section(subelem):
            return True
    return False

def normalize_txt(txt):
    return normalize('NFKD', txt).lower().strip()

def clean_titles(root):
    """Set all the <title>s as the parent node's attribute and remove it from the parent.
    Should be called first.
    """
    to_remove = []
    for title_parent in root.findall('.//title/..'):
        title, subtitle = title_parent.find('title'), title_parent.find('subtitle')
        for t in [title, subtitle]:
            if t != None and title_parent.tag != 'document':
                title_parent.set(t.tag, normalize_txt(''.join(t.itertext())))
                to_remove.append((title_parent, title))

    for p,c in to_remove:
        p.remove(c)

def extract_abst(doc, titlepage):
    '''Extract abstract and move the element to within <document>
    '''
    abstract = titlepage.find('abstract')
    if abstract:
        titlepage.remove(abstract)
        doc.insert(3,abstract)
        flatten_elem(abstract)

def rename_rank1secs(rank1elem):
    if 'section' in rank1elem.tag:
        rank1elem.tag = 'section'
    elif rank1elem.tag in ('chapter', 'part'):
        for elem in rank1elem:
            if is_section(elem):
                elem.tag = 'section' 
        rank1elem.tag = 'chapter'

def clean(root):
    toremove = []
    remove_useless(root)
    clean_titles(root)
    for rank1elem in root:  # 1st pass
        if rank1elem.tag in keeplist: # titles, abstracts, 
            if rank1elem.tag == 'titlepage':
                extract_abst(root, rank1elem)
            flatten_elem(rank1elem)
                
        elif is_section(rank1elem):
            rename_rank1secs(rank1elem)
            clean_sec(rank1elem)

        else:
            toremove.append((root, rank1elem)) # Don't modify it during iteration!

    for p, c in toremove:
        try:
            p.remove(c)
        except ValueError:
            continue

    add_abstract(root)

def is_empty(elem):
    try:
        txt = ''.join(elem.itertext())
        if txt.strip() == '':
            return True
    except TypeError:
        print([chunk for chunk in elem.itertext()])
    return False

def postcheck(root, errlog):
    err = False
    errlog.write(xmlpath + ' \n')

    secdict = {'abstract': root.findall('abstract'), 'secs':root.findall('section')}
    for title in secdict:
        elems = secdict[title]

        if title == 'secs' and elems == []:
            elems = root.findall('./chapter/section')

        if len(elems) == 0: # If element not found
            err = True
            # print(title + ' absent: ' + xmlpath)
            errlog.write(title + ' absent. ')
            continue
        
        # If the node exists but is empty
        for elem in elems:
            if is_empty(elem):
            # try:
            #     txt = ''.join(elem.itertext()) 
            # except TypeError:
            #     print([chunk for chunk in elem.itertext()])
            # if txt == '':
                err = True
                # print('Empty ' + title + ' :' + xmlpath)
                errlog.write('Empty ' + title + '. ')
                                    
    if not err:
        errlog.write('OK. ')
    errlog.write('\n ================================== \n')
            
def get_root(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    ignore_ns(root)
    return tree, root

if __name__ == "__main__":
    VERBOSE, REPORT_EVERY = True, 100
    xmls = [fn for fn in listdir(rawxmls_path) if fn[-4:] == '.xml']
    # xmls = ['=hep-ph0002094.xml']
    
    begin = time.time()

    with open(cleanlog_path, 'w') as cleanlog:
        for i, xml in enumerate(xmls):
            xmlpath = join(rawxmls_path, xml)
            try:
                tree, root = get_root(xmlpath)
            except ET.ParseError:
                print('Skipped: ParseError at %s' % xmlpath)
                cleanlog.write(xmlpath + ' \n' + 'ParseError. \n' + '================================== \n')
                continue
            clean(root)
            postcheck(root, cleanlog)
            tree.write(join(cleanedxml_path, xml))

            if VERBOSE:
                if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmls):
                    print('%s of %s ...' % (i+1, len(xmls)))

    t = time.time() - begin
    t = t/60
    print(len(xmls), 'files in %s mins' % t)