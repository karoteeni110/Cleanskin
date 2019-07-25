import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from os.path import join, basename
from os import listdir
from shutil import copy, copytree
import time
from xmlCleaner import ignore_ns, get_root, get_ttn

def clean(root, tags = ['cite', 'Math', 'figure', 'table', 'ERROR', 'pagination', 'rdf', 'index', 'toctitle', 'tags', 'tag', 'equation', 'equationgroup', 'ref']):
    rmlist = []
    for tag in tags:
        parents = root.findall('.//%s/..' % tag)
        for parent in parents:
            if parent:
                child = parent.findall(tag)
                rmlist.append((parent, child))
    for p,children in rmlist:
        print(p, children)
        for child in children:
            p.remove(child)

# def getparent(elem):
#     return elem.findall('..')

def title2attrib(root):
    '''Remove <title> & <subtitle> after setting the title name as the parent node's attribute
    '''
    tt_buffer = {}
    for subelem in root:
        if subelem.tag in ('title', 'subtitle'):
            tt_buffer[subelem.tag] = get_ttn(subelem)
    root.clear()
    root.attrib = tt_buffer

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
        clean(root)
        tree.write(join(results_path, xml))

    