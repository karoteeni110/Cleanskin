import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
import time
from xmlCleaner import get_root, postcheck


keeplist = ['title', 'abstract', 'creator', 'keywords', 'para', 'theorem', 'proof', 'appendix', 'bibliography', 'titlepage']
sec_tags = ['section', 'chapter', 'subsection', 'subsubsection', 'paragraph', 'subpragraph']
useful_attribs = ['title', 'subtitle']

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
    if elem.tag in sec_tags and have_title(elem):
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

def clean_titles(root):
    """Set all the <title>s as the parent node's attribute and remove it from the parent.
    Should be called first
    """
    title_elems = []
    for title_parent in root.findall('.//title/..'):
        title, subtitle = title_parent.find('title'), title_parent.find('subtitle')
        for t in [title, subtitle]:
            if t != None:
                title_parent.set(t.tag, ''.join(t.itertext()))
                title_elems.append((title_parent, title))
    for p,c in title_elems:
        p.remove(c)

def extract_abst(doc, titlepage):
    '''Extract abstract and move the element to within <document>
    '''
    abstract = titlepage.find('abstract')
    if abstract:
        titlepage.remove(abstract)
        doc.insert(3,abstract)
        flatten_elem(abstract)

def clean(root):
    toremove = []
    remove_useless(root)
    clean_titles(root)
    for rank1elem in root:  # 1st pass
        if rank1elem.tag in keeplist: # if element in ``keeplist``, texify it; remove otherwise
            if rank1elem.tag == 'titlepage':
                extract_abst(root, rank1elem)
            flatten_elem(rank1elem)
                
        elif is_section(rank1elem):
            if 'section' in rank1elem.tag:
                rank1elem.tag = 'section'
            clean_sec(rank1elem)
        else:
            toremove.append((root, rank1elem)) # Don't modify it during iteration!

    for p, c in toremove:
        try:
            p.remove(c)
        except ValueError:
            print(p, c)

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
            tree.write(join(results_path, xml))

            if VERBOSE:
                if (i+1) % REPORT_EVERY == 0 or i+1 == len(xmls):
                    print('%s of %s collected.' % (i+1, len(xmls)))

    t = time.time() - begin
    t = t/60
    print(len(xmls), 'files in %s mins' % t)