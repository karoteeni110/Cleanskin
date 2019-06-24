"""
Ruling out the <acknowledgement> and <references> sections.
Flattening the subsections.
Handles at most one layer subsection structure.
"""
import xml.etree.ElementTree as ET
from collections import defaultdict
from unicodedata import normalize

def recur_rm(parent):
    '''
    Check and remove the acknowledgement sec in the children.
    '''
    for child in list(parent): # If no child, list is empty
        if child.get('text', False).lower() in ('acknowledgements', 'references', 'bibliography'):
            parent.remove(child)

def flatten(parent):
    '''
    Organize subsections into one whole section.
    '''
    if parent.tag == 'outline':
        for subsec in list(parent): # If no child, list is empty
            parent.set('_note', parent.get('_note', '') + subsec.attrib['_note'] + ' \n') # don't use defaultdict!
            parent.remove(subsec)

# title, abstract, sections['introduction'] ... 
fpath = sys.arg[1] # Change This
data = open(fpath,'r')
tree = ET.parse(data)
root = tree.getroot()

for child in root: # head, body
    if child.tag == 'head':
        title = child[0].text
        abstract = child[1].text

    elif child.tag == 'body':
        for outline in child.iter():
            recur_rm(outline)
            flatten(outline)

tree.write(sys.arg[2])