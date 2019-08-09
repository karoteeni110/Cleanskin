import xml.etree.ElementTree as ET
from paths import cleanedxml_path
from headingStats import get_headings
from os.path import join

# === The 9 cates we want sections to be put into ===
def is_abstract(elem):
    if elem.tag == 'abstract' or elem.get('title') == 'abstract':
        return True
    return False

def is_intro(elem):
    if elem.get('title') == 'introduction':
        return True
    return False

def is_bg():
    pass 

def is_rltwork():
    pass

def is_methods():
    pass 

def is_results():
    pass 

def is_discussion():
    pass

def is_conclusion():
    pass

def is_backmatter():
    pass

# == Auxilary functions

def is_bib_sec(secelem):
    if secelem.tag == 'bibliography' or secelem.get('title') in ('bibliography', 'references', 'reference'):
        return True
    return False