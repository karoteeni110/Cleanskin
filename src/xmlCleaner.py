"""
`texify_*` funcs flatten the argument and returns None. Elements after ``texify`` wouldn't have child nodes.
`clean_*` funcs may keeps some subelements as the argument's child. Returns None.
`*_text`s collect and return the text within the argument without doing any change to it. Returns str.
"""

import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path
from os.path import join, basename
from shutil import copy, copytree

def ignore_ns(root):
    '''
    Clean namespace in the node's tag. Should be called in the first place.
    '''
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

def opening(elem):
    if elem.text:
        return elem.text
    else:
        return ''

def inlinepara_text(inpara):
    txt = opening(inpara)
    for elem in list(inpara):
        if elem.tag == 'para':
            texify_para(elem)
            txt += ' ' + elem.text
        elif elem.tag == 'theorem':
            clean_section(elem)
            txt += ' ' + elem.text
        elif elem.tag == 'float':
            txt += ' ' + float_text(elem)
    return txt

def p_text(p, keeplist=[]):
    """
    Captures all the text within <p> and its trailing,
    skipping all intermediate tags except <text>, <note> and <inline-para>.

    Return the concatenated str.
    """
    txt = opening(p)    
    for child in list(p):
        if child.tag in ('note', 'text'):
            txt += ' ' + p_text(child)
        if child.tag == 'inline-para':
            txt += ' ' + inlinepara_text(child)
        elif child.tag in keeplist and child.text: # default: Skips all intermediate elements
            txt += ' ' + child.text
        if child.tail:
            txt += ' ' + child.tail
    if p.tail:
        txt += ' ' + p.tail
    return txt

def listing_text(lsting):
    txt = opening(lsting)
    for elem in list(lsting):
        if elem.tag == 'listingline':
            txt += ' ' + p_text(elem)
    if lsting.tail:
        txt += ' ' + lsting.tail
    return txt

def float_text(flt):
    # results/latexml/=1701.00757.xml
    txt = opening(flt)
    for elem in list(flt):
        if elem.tag == 'listing':
            txt += ' ' + listing_text(elem)
        elif elem.tag in ('toccaption', 'caption'):
            txt += ' ' + p_text(elem)
    if flt.tail:
        txt += ' ' + flt.tail
    return txt

def get_ttn(ttelem):
    '''
    Get title str from title element.
    '''
    return p_text(ttelem).strip()

def texify_para(para):
    '''
    Collects all the <p>s and extract the text from them.
    Clears all the content in the element, and set the text to ``text``. 

    Useful subelements: <p>
    '''
    txt = opening(para)
    for p in list(para):
        if p.tag == 'p':
            txt += ' ' + p_text(p) 
        elif p.tag == 'inline-para':
            txt += ' ' + inlinepara_text(p)
        elif p.tag in ('itemize', 'description'):
            txt += ' ' + descrip_text(p)
        elif p.tag == 'quote':
            txt += ' ' + quote_text(p)

    para.clear()
    para.tag = 'para' # Change the element tag to 'para': toctitle, titlepage
    para.text = txt

def item_text(item):
    # Useful: <tags>, <para>
    txt = opening(item)
    for elem in list(item):
        if elem.tag == 'tags': 
            for tag in list(elem):
                for i in list(tag):
                    if i.tag == 'text':
                        txt += ' ' + i.text + ':'
        elif elem.tag == 'para':
            texify_para(elem)
            txt += elem.text
    if item.tail:
        txt += ' ' + item.tail
    return txt

def descrip_text(des): 
    # Useful: item
    txt = opening(des)
    for elem in list(des):
        if elem.tag == 'item': # should be trivial
            txt += ' ' + item_text(elem)
        if elem.tail:
            txt += elem.tail
    if des.tail:
        txt += ' ' + des.tail
    return txt

def quote_text(quote):
    txt = opening(quote)
    for elem in list(quote):
        if elem.tag == 'p':
            txt += ' ' + p_text(elem)
        elif elem.tag == 'quote':
            txt += ' ' + quote_text(elem)
        elif elem.tag == 'listing':
            txt += ' ' + listing_text(elem)
        elif elem.tag == 'description':
            txt += ' ' + descrip_text(elem)
    if quote.tail:
        txt += ' ' + quote.tail
    return txt

def clean_section(secelem):
    # Clear the ``secelem`` and set <title> as `attrib`, <para>s into `text`,
    # keeps subelements like <sections> after texifying them.

    # Useful: title, para, subsection, subsubsection, theorem, subparagraph, 
    # proof, acknowledgements, paragraph, bibliography, note, float

    # Ignore: indexmark, figure, bibitem, TOC, tags, toctitle, table, pagination, ERROR
    txt, titles, subsecs = [], [], []
    for elem in list(secelem):
        if elem.tag == 'para':
            texify_para(elem)
            txt.append(elem.text)
        elif elem.tag == 'float':
            txt.append(float_text(elem))
        elif elem.tag in ('title', 'subtitle'):
            titles.append((elem.tag, get_ttn(elem)))
        elif elem.tag in ('subsection', 'subparagraph', 'theorem', 'proof', 'paragraph', 'subsubsection'):
            clean_section(elem)
            if elem.tag in ('theorem', 'proof'):
                elem.set('title', elem.tag)
            elem.tag = 'subsection' # uniform tag
            subsecs.append(elem)
        elif elem.tag == 'note': 
            txt = p_text(elem)
            elem.clear()
            elem.text = txt
        elif elem.tag in ('acknowledgements', 'bibliography'):
            elem.clear()
            subsecs.append(elem)

    secelem.clear()
    for title_name,title in titles:
        secelem.set(title_name, title)
    for subsec in subsecs:
        secelem.append(subsec)
    secelem.text = ' '.join(txt)

def clean_chapter(chapelem):
    for elem in list(chapelem):
        if elem.tag == 'para':
            texify_para(elem)
        elif elem.tag == 'toctitle':
            title = p_text(elem)
        elif elem.tag in ('subsection', 'subparagraph', 'section', 'subsubsection'):
            clean_section(elem)
            elem.tag = 'section'
    chapelem.attrib = dict()
    chapelem.set('title', title)
    
def texify_abstract(ab):
    '''
    Collect the text at the beginning, within subelements and their trailing to ``txt``,
    clear the element,
    and finally, set the text to ``txt``.
    
    Useful children: p, description, quote, inline-para, section, itemize
    '''
    txt = opening(ab)
    for elem in list(ab):
        if elem.tag == 'p':
            txt += ' ' + p_text(elem)
        elif elem.tag in ('itemize', 'description', 'enumerate'):
            txt += ' ' + descrip_text(elem)
        elif elem.tag == 'inline-para':
            txt += ' ' + inlinepara_text(elem)
        elif elem.tag == 'quote':
            txt += ' ' + quote_text(elem)
    ab.clear()
    ab.text = txt # ignore: break, pagination, ERROR, equation, ...
            
def clean(root):
    useless = []
    for child in root:
        if child.tag in ('title', 'subtitle','keywords'):
            content = p_text(child) # clear <break>
            child.clear()
            child.text = content
        elif child.tag == 'abstract':
            texify_abstract(child)
        elif child.tag in ('section', 'paragraph', 'subparagraph', 'subsection'):
            clean_section(child)
            child.tag = 'section'
        elif child.tag in ('para', 'toctitle', 'titlepage') : 
            # Useful: p, inline-para XXX: post-process!
            texify_para(child)
            if child.text == None or re.match(r'^[\w+]+$', child.text) == None: # If empty, remove
                useless.append((root, child))
            child.tag = 'para'
        elif child.tag == 'note':
            # Useful children: p
            notetxt = p_text(child)
            child.clear()
            child.text = notetxt
        elif child.tag == 'glossarydefinition':
            pass
        
        elif child.tag in ('chapter', 'part'):
            clean_chapter(child)
            child.tag = 'chapter'
        elif child.tag in ('theorem', 'proof'):
            clean_section(child)
            child.tag = 'section'
        elif child.tag in ('acknowledgements', 'bibliography', 'appendix', 'creator', 'index', 'date', 'float'):
            child.clear()
        else: # Remove <figure>, <part>, <classification>, <table>, <ERROR>, <appendix>, <TOC>, <pagination>, <rdf>, <tags>
            useless.append((root,child))
    
    for par, chi in useless:
        par.remove(chi) 
        

if __name__ == "__main__":
    # hep-ph0001047.xml
    # tree = ET.parse(join(data_path, 'out.xml'))
    # XXX:subparagraph case: =hep-th0002024.xml
    xmlpath = '/home/local/yzan/Desktop/Cleanskin/results/latexml/=math-ph0002040.xml'

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
    tree.write(join(results_path, 'quote.xml'))
    
