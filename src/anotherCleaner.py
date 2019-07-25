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
may_contain_subsecs = ['section', 'chapter', 'subsection', 'subsubsection', 'paragraph', 'subpragraph']


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

def texify(root):
    toremove = []
    for rank1elem in root:
        if rank1elem.tag in keeplist:
            # TODO: if there is no subsection -type elements
            txt = ''.join(rank1elem.itertext())
            title, subtitle = rank1elem.find('title'), rank1elem.find('subtitle')
            rank1elem.clear()
            rank1elem.text = txt
            for t in [title, subtitle]:
                if t != None:
                    rank1elem.set(t.tag, ''.join(t.itertext()))
            if rank1elem.tag in may_contain_subsecs and rank1elem.get('title', None):
                rank1elem.tag = 'section'
        else:
            toremove.append(rank1elem) # Don't modify 
    for i in toremove:
        root.remove(i)

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

    