import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
import time
from xmlCleaner import ignore_ns, get_root, get_ttn

def remove_useless(root, tags = ['cite', 'Math', 'figure', 'table', 'ERROR', 'pagination', 'rdf', 'index', \
                    'toctitle', 'tags', 'tag', 'equation', 'equationgroup', 'ref', 'break', 'resource']):
    """Remove useless elements with keeping the trailing texts
    """
    rmlist = []
    for tag in tags:
        parents = root.findall('.//%s/..' % tag)
        for parent in parents:
            if parent:
                child = parent.findall(tag)
                rmlist.append((parent, child))
    for p,children in rmlist:
        for child in children:
            p.remove(child)

# def getparent(elem):
#     return elem.findall('..')

def texify(root):
    toremove = []
    for elem in root:
        if elem.tag in ['title', 'abstract', 'section', 'creator', 'keywords', 'titlepage', 'para', 'chapter', 'bibliography', \
                    'paragraph', 'subparagraph', 'subsection', 'appendix', 'theorem', 'proof', 'subsubsection']:
            txt = ''.join(elem.itertext()) # TODO: move titles
            title, subtitle = elem.find('title'), elem.find('subtitle')
            if title != None:
                print(''.join(title.itertext()))
            elem.clear()
            elem.text = txt
            for t in [title, subtitle]:
                print(elem, t)
                if t != None:
                    elem.set(t.tag, ''.join(t.itertext()))
        else:
            toremove.append(elem)
    for i in toremove:
        root.remove(i)

if __name__ == "__main__":
    # xmls = [fn for fn in listdir(rawxmls_path) if fn[-4:] == '.xml']
    xmls = ['=hep-ph0001264.xml']

    for xml in xmls:
        xmlpath = join(rawxmls_path, xml)
        try:
            tree, root = get_root(xmlpath)
        except ET.ParseError:
            print('Skipped: ParseError at %s' % xmlpath)
            # cleanlog.write(xmlpath + ' \n' + 'ParseError. \n' + '================================== \n')
            continue
        remove_useless(root)
        # texify(root)
        tree.write(join(results_path, xml))

    