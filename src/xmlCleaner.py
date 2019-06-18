"""
Rules out the <acknowledgement> and <references> sections.
Flattens the subsections.

Does NOT assume single layer subsection structure.
"""
import xml.etree.ElementTree as ET
from unicodedata import normalize
from os.path import basename, join
from paths import within_results
import sys

fpath = sys.argv[1] # abspath of the xml
if fpath[-4:] != '.xml':
    raise AssertionError ("Not XML!")
data = open(fpath,'r')
tree = ET.parse(data)
root = tree.getroot()

def recur_rm(parent):
    '''Check and remove the acknowledgement sec in the children.
    '''
    for child in list(parent): # If no child, list is empty
        if child.get('text', False).lower() in ('acknowledgements', 'references', 'bibliography'):
            parent.remove(child)

def flatten(parent):
    '''Organize subsections into one whole section.
    '''
    if parent.tag == 'outline':
        for subsec in list(parent): # If no child, list is empty
            parent.set('_note', parent.get('_note', '') + subsec.attrib['_note'] + ' \n') # don't use defaultdict!
            parent.remove(subsec)

# title, abstract, sections['introduction'] ... 
for child in root: # head, body
    if child.tag == 'body':
        for outline in child.iter():
            recur_rm(outline)
            flatten(outline)

outname = join(within_results('/final'), basename(fpath))
tree.write(outname) # Overwrite the original file