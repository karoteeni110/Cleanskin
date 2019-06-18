"""
Ruling out the <acknowledgement> and <references> sections.
Flattening the subsections.

Handles at most one layer subsection structure.
"""
import xml.etree.ElementTree as ET
from collections import defaultdict
from unicodedata import normalize

fpath = '/home/yzan/Desktop/Cleanskin/results/0002/0002xml/astro-ph0002005.xml'
data = open(fpath,'r')
tree = ET.parse(data)
root = tree.getroot()

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
sections = defaultdict(str)
for child in root: # head, body
    if child.tag == 'head':
        title = child[0].text
        abstract = child[1].text

    elif child.tag == 'body':
        for outline in child.iter():
            recur_rm(outline)
            flatten(outline)

            # if secOrSubsec.attrib['text'].lower() in ('acknowledgements', 'references'):
            #     secOrSubsec.clear()
            #     continue
        # for outline in child:
        #     if len(outline.attrib.keys()) == 2: # 'text', '_note'
        #         sections[outline.attrib['text'].lower()] = outline.attrib['_note']
        #     elif len(outline.attrib.keys()) == 1:
        #         for subsec in outline:
        #             sections[outline.attrib['text'].lower()] += '\n' + subsec.attrib['_note']

    # print('Title', title)
    # print('==')
    # print('abstract', abstract)
    # print('==')
tree.write('/home/yzan/Desktop/0002005.xml')
# print(normalize(u'\xa0', sections['introduction']))