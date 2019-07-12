'''
Organize special-case XMLs so that they can be cleaned by ``xmlCleaner.py``
'''
import xml.etree.ElementTree as ET
import sys
from paths import data_path, results_path, data0001, data0002, data1701
from os.path import join, basename
from xmlCleaner import ignore_ns

def mv_secs_in_abstract(root):
    # abstract/section in ``=hep-th0002028.xml``
    # Solution: move the <section> in <abstract> to <document>
    return root

if __name__ == "__main__":
    path = join(data0002, '=hep-th0002028.xml')
    outpath = join(results_path, '=hep-th0002028.xml')
    tree = ET.parse(path)
    root = tree.getroot()
    ignore_ns(root)
    mv_secs_in_abstract(root)
    tree.write(outpath)