"""
`texify_*` funcs flatten the argument. Elements after ``texify`` wouldn't have child nodes.
`clean_*` funcs may keeps some subelements as the argument's child.
`*_text`s collect and return the text within the argument without doing any change to it.
"""

import xml.etree.ElementTree as ET
import sys
from paths import data_path, results_path
from os.path import join, basename
from shutil import copy, copytree


def ignore_ns(root):
    '''
    Clean namespace in the node's tag. 
    Should be called in the first place.
    '''
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

def flatten_text(root, keeplist=[]):
    """
    TODO: ``keeplist``
    XXX: Seems it overlaps with ``texify_para()``; delete this?
    
    Flatten root: extract the beginning, in-between and ending text in ``root``, where:
    beginning text: ``root.text``
    in-between text: ``[child.text+child.tail for child in root]``
    end text: the last ``child.tail``

    XXX:  Assumes child nodes don't have deeper structure.

    """
    if root.text:
        txt = [root.text.strip('\n')]
    else:
        txt = []
    for child in root:
        if child.tag in keeplist and child.text:
            txt.append(child.text)
        if child.tail: 
            txt.append(child.tail)
    return ' '.join(txt)

def p_text(p):
    """
    Captures all the text within <p> and its trailing,
    skipping all intermediate tags except <text> and <note>.

    Return the concatenated str.
    """
    if p.text:
        txt = [p.text.strip('\n')] # head text
    else:
        txt = []
    for child in list(p):
        if child.tag in ('text', 'note'): # should be trivial
            txt.append(flatten_text(child))
        if child.tail:
            txt.append(child.tail.strip('\n'))
    if p.tail:
        txt.append(p.tail)
    
    return ' '.join(txt)

def itemize_text(itemize_elem):
    return ''

# def ps_text(ps):
#     '''
#     XXX: seperate <inline-para>
#     Iterating ps (a list of <p> elements), passing them to p_text
#     and return a str.
#     '''
#     pstext = []
#     for p in ps:
#         if p.tag == 'p': # should be trivial
#             pstext.append(p_text(p))
#         if p.tail:
#             pstext.append(p.tail)
#     return ' '.join(pstext)
def inlinepara_text(inpara):
    if inpara.text:
        txt = inpara.text
    else:
        txt = ''
    
    for elem in list(inpara):
        if elem.tag == 'para':
            texify_para(elem)
            txt += elem.text
        elif elem.tag == 'theorem':
            clean_section(elem)
            txt += elem.text
        


def texify_para(para):
    '''
    Collects all the <p>s and extract the text from them.
    Clears all the content in the element, and set the text to ``text``. 

    Useful subelements: <p>
    '''
    if para.text:
        txt = para.text.strip('\n') # head text
    else:
        txt = ''
    # ps = [elem for elem in list(para) if elem.tag in ('p', 'inline-para')] # trailing text included
    # txt += ps_text(ps)
    
    for p in list(para):
        if p.tag == 'p':
            txt += p_text(p) 
        if p.tag == 'inline-para':
            txt += inlinepara_text(p)
        if p.tag == 'itemize':
            txt += itemize_text(p)

    para.clear()
    para.tag = 'para' # Change the element tag to 'para': toctitle, titlepage
    para.text = txt

# def paras_text(paras):
#     '''
#     Returns elem.text for each element in paras list.
#     If there are other subelem in elem, flatten it with ``para_texify()``.
#     '''
#     for elem in paras:
#         if len(list(elem)) != 0:
#             if elem.tag == 'para':
#                 texify_para(elem)
#     return ' '.join([elem.text for elem in paras])

def get_ttn(ttelem):
    '''
    Get title str from title element.
    '''
    return flatten_text(ttelem)


def clean_section(secelem):
    # Clear the ``secelem`` and set <title> as `attrib`, <para>s into `text`,
    # keeps subelements like <sections> after texifying them.

    # Useful: title, para, subsection, subsubsection, 
    # subparagraph, proof(?), acknowledgements(?)
    # paragraph, bibliography(?), note, proof(?), float(?), indexmark(?), theorem
    paras, titles, subsecs = [], [], []
    for elem in list(secelem):
        if elem.tag == 'para':
            paras.append(elem)
        elif elem.tag in ('title', 'subtitle'):
            titles.append((elem.tag, get_ttn(elem)))
        elif elem.tag in ('subsection', 'subparagraph', 'theorem', 'proof'):
            clean_section(elem)
            elem.tag = 'subsection'
            subsecs.append(elem)

    secelem.clear()
    for title_name,title in titles:
        secelem.set(title_name, title)
    for subsec in subsecs:
        secelem.append(subsec)
    secelem.text = paras_text(paras)

def clean_chapter(chapelem):
    for elem in list(chapelem):
        if elem.tag == 'para':
            texify_para(elem)
        elif elem.tag == 'toctitle':
            title = flatten_text(elem)
        elif elem.tag in ('subsection', 'subparagraph', 'section', 'subsubsection'):
            clean_section(elem)
            elem.tag = 'section'
    chapelem.attrib = dict()
    chapelem.set('title', title)

def enum_text(enum):
    return ''

def texify_abstract(ab):
    '''
    Collect the text at the beginning, within subelements and their trailing to ``txt``,
    clear the element,
    and finally, set the text to ``txt``.
    '''
    if ab.text:
        txt = ab.text
    else:
        txt = ''
    for elem in list(ab):
        if elem.tag == 'p':
            txt += ' ' + p_text(elem)
        elif elem.tag == 'itemize':
            txt += ' ' + itemize_text(elem)
        elif elem.tag == 'enumerate':
            txt += ' ' + enum_text(elem) 
        elif elem.tag == 'inline-para':
            txt += ' ' + inlinepara_text(elem)
        elif elem.tag == 'description':
            pass
        elif elem.tag == 'quote':
            pass
    ab.clear()
    ab.text = txt # ignore: break, pagination, ERROR, equation, ...
            
def clean(root):
    useless = []
    for child in root:
        if child.tag in ('title', 'subtitle','keywords'):
            continue
        elif child.tag in ('acknowledgements', 'bibliography'):
            child.clear()
        elif child.tag == 'abstract':
            # Useful children: p, 
            # description, quote, inline-para, section, itemize
            texify_abstract(child)
        elif child.tag in ('section', 'paragraph', 'subparagraph'):
            # Useful: title, para, subsection, 
            # subsubsection, subparagraph, proof(?), acknowledgements(?)
            # paragraph, bibliography(?), note, proof(?), float(?), indexmark(?), theorem
            clean_section(child)
        elif child.tag == 'note':
            # Useful children: p
            notetxt = p_text(child)
            child.clear()
            child.text = notetxt
        elif child.tag in ('para', 'toctitle', 'titlepage') : 
            # Useful: p, inline-para
            texify_para(child)
            if not child.text:
                useless.append((root, child))
            child.tag = 'para'
        elif child.tag == 'chapter':
            clean_chapter(child)
        else: # Remove <creator>, <date>, <resource>, ... <theorem>(?)
            useless.append((root,child))
    
    for par, chi in useless:
        par.remove(chi) 
        

if __name__ == "__main__":
    # hep-ph0001047.xml
    # tree = ET.parse(join(data_path, 'out.xml'))
    # XXX:subparagraph case: =hep-th0002024.xml
    xmlpath = '/home/local/yzan/Desktop/Cleanskin/results/latexml/=astro-ph0001248.xml'
    # xmlpath = '/home/local/yzan/Desktop/Cleanskin/results/latexml/=astro-ph0002442.xml'
    errcasepath = join(results_path, 'latexml/errcp')
    try:
        tree = ET.parse(xmlpath)
        root = tree.getroot()
        ignore_ns(root)
    except ET.ParseError:
        print('cp ParseError at %s' % xmlpath)
        copy(xmlpath, join(errcasepath, basename(xmlpath)))

    # keep_taglist = ['title', 'abstract', 'section', 'subsection', 'chapter', \
    #      'paragraph', 'subparagraph', 'para', 'p' ,'note', ]
    # useless = []

    clean(root)
    tree.write(join(results_path, 'test.xml'))
    
