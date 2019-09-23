import xml.etree.ElementTree as ET
import re
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

def is_bg(elem):
    if elem.get('title') == 'background':
        return True
    return False 

def is_rltwork(elem):
    if elem.get('title') == 'related work':
        return True
    return False

def is_methods(elem):
    if elem.get('title') == 'methods':
        return True
    return False 

def is_results(elem):
    if elem.get('title') == 'results':
        return True
    return False 

def is_discussion(elem):
    if elem.get('title') == 'discussion':
        return True
    return False

def is_conclusion(elem):
    if elem.get('title') == 'conclusion':
        return True
    return False

def is_backmatter(elem):
    if re.match(r'(acknowledg(e)ment(s)|reference)', elem.get('title'), flags=re.I):
        return True
    elif elem.tag.lower() == 'bibliography':
        return True
    return False

# == Auxilary functions

def is_bib_sec(secelem):
    if secelem.tag == 'bibliography' or secelem.get('title') in ('bibliography', 'references', 'reference'):
        return True
    return False