import xml.etree.ElementTree as ET
from paths import cleanedxml_path
from headingStats import get_title
from os.path import join

def is_abstract(elem):
    if elem.tag == 'abstract' or get_title(elem) == 'abstract':
        return True
    return False

def is_intro(elem):
    if get_title(elem) == 'introduction':
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

