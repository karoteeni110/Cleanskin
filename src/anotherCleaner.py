import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
import time
from xmlCleaner import ignore_ns, get_root, get_ttn


keeplist = ['title', 'abstract', 'section', 'creator', 'keywords', 'titlepage', 'para', 'chapter', 'bibliography', \
                    'paragraph', 'subparagraph', 'subsection', 'appendix', 'theorem', 'proof', 'subsubsection']
sec_tags = ['section', 'chapter', 'subsection', 'subsubsection', 'paragraph', 'subpragraph', 'appendix', 'bibliography']


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

def flatter_elem(elem):
    txt = ''.join(elem.itertext())
    elem.clear()
    elem.text = txt

def clean_sec(sec):
    for subelem in sec:
        flatter_elem(subelem)

def have_title(elem):
    if elem.findall('title') != []:
        return True
    else:
        return False

def have_subsec(elem):
    for subelem in elem:
        if subelem.tag in sec_tags and have_title(subelem):
            return True
    return False

def texify(root):
    toremove = []

    for rank1elem in root:  # 1st pass
        if rank1elem.tag in keeplist: # if element in ``keeplist``, texify it; remove otherwise

            
            if have_subsec(rank1elem):
                for subelem in rank1elem:
                    if subelem.tag in sec_tags:
                        clean_sec(subelem)
                    else:
                        flatter_elem(rank1elem)

            elif rank1elem.tag in sec_tags: # sec that don't have subsecs 
                clean_sec(rank1elem)
                rank1elem.tag = 'section'
            else:
                flatter_elem(rank1elem)
        else:
            toremove.append((root, rank1elem)) # Don't modify it during iteration!

    for title_parent in root.findall('.//title/..'): # 2nd pass
        title, subtitle = title_parent.find('title'), title_parent.find('subtitle')
        for t in [title, subtitle]:
            if t != None:
                title_parent.set(t.tag, ''.join(t.itertext()))
                toremove.append((title_parent, title))

    
    for p, c in toremove:
        try:
            p.remove(c)
        except ValueError:
            print(p, c)
if __name__ == "__main__":
    # xmls = [fn for fn in listdir(rawxmls_path) if fn[-4:] == '.xml']
    xmls = ['=math0001145.xml']

    for xml in xmls:
        xmlpath = join(rawxmls_path, xml)
        try:
            tree, root = get_root(xmlpath)
        except ET.ParseError:
            print('Skipped: ParseError at %s' % xmlpath)
            # cleanlog.write(xmlpath + ' \n' + 'ParseError. \n' + '================================== \n')
            continue
        remove_useless(root)
        texify(root)
        tree.write(join(results_path, xml))

    