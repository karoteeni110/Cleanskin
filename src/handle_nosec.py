'''
Check and re-clean the xmls that do not have sections.
'''
import xml.etree.ElementTree as ET
import sys
from paths import cleanedxml_path
from os.path import join, basename
from newCleaner import get_root
from errortypes import have_intro_in_xml

def get_introelem_features(introelem):
    pass

# def get_parent_

def look_like_title(features, elem_parent, elem):
    pass
    # features[parent]

if __name__ == "__main__":
    xmlpaths = [join(cleanedxml_path, '=gr-qc0002029.xml')]
    for xmlpath in xmlpaths:
        if have_intro_in_xml(xmlpath):
            tree, root = get_root(xmlpath)
            get_title_features(root)

