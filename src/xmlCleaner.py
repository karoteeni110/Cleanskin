"""
`texify_*` funcs flatten the argument and returns None. Elements after ``texify`` wouldn't have child nodes.
`clean_*` funcs may keeps some subelements as the argument's child. Returns None.
`*_text`s collect and return the text within the argument without doing any change to it. Returns str.
"""

import xml.etree.ElementTree as ET
import sys, re
from paths import data_path, results_path, rawxmls_path, cleanlog_path, cleanedxml_path
from os.path import join, basename
from os import listdir
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
    for elem in inpara:
        if elem.tag == 'para':
            texify_para(elem)
            txt += ' ' + elem.text
        elif elem.tag == 'theorem':
            clean_section(elem)
            txt += ' ' + elem.text
        elif elem.tag == 'float':
            txt += ' ' + float_text(elem)
    return txt

def p_text(p, dontskip=[]):
    """
    Captures all the text within <p> and its trailing,
    skipping all intermediate tags except <text>, <note> and <inline-para>.

    Return the concatenated str.
    """
    txt = opening(p)    
    for child in p:
        if child.tag in ('p', 'note', 'text', 'emph'):
            txt += ' ' + p_text(child)
        if child.tag == 'inline-para':
            txt += ' ' + inlinepara_text(child)
        elif child.tag in dontskip and child.text: # get text from simple elems in ``dontskip``
            txt += ' ' + child.text
        if child.tail:
            txt += ' ' + child.tail
    if p.tail:
        txt += ' ' + p.tail
    return txt

def listing_text(lsting):
    txt = opening(lsting)
    for elem in lsting:
        if elem.tag == 'listingline':
            txt += ' ' + p_text(elem)
    if lsting.tail:
        txt += ' ' + lsting.tail
    return txt

def float_text(flt):
    # results/latexml/=1701.00757.xml
    txt = opening(flt)
    for elem in flt:
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
    '''
    txt = opening(para)
    for p in para:
        if p.tag in ('p', 'note', 'text', 'personname', 'glossaryphrase') :
            txt += ' ' + p_text(p) 
        elif p.tag == 'inline-para':
            txt += ' ' + inlinepara_text(p)
        elif p.tag in ('itemize', 'description'):
            txt += ' ' + descrip_text(p)
        elif p.tag == 'quote':
            txt += ' ' + quote_text(p)
    para.clear() # Change the element tag to 'para': toctitle, titlepage
    para.text = txt

def item_text(item):
    # Useful: <tags>, <para>
    txt = opening(item)
    for elem in item:
        if elem.tag == 'tags': 
            for tag in elem:
                for i in tag:
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
    for elem in des:
        if elem.tag == 'item': # should be trivial
            txt += ' ' + item_text(elem)
        if elem.tail:
            txt += elem.tail
    if des.tail:
        txt += ' ' + des.tail
    return txt

def quote_text(quote):
    txt = opening(quote)
    for elem in quote:
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

def texify(elem, elemtext):
    if elemtext != None:
        elem.clear()
        elem.text = elemtext


def clean_section(secelem):
    # Clear the ``secelem`` and set <title> as `attrib`, <para>s into `text`,
    # keeps subelements like <sections> after texifying them.

    # Useful: title, para, subsection, subsubsection, theorem, subparagraph, 
    # proof, acknowledgements, paragraph, bibliography, note, float

    # Ignore: indexmark, figure, bibitem, TOC, tags, toctitle, table, pagination, ERROR
    # txt, titles, subsecs = [], [], []
    secelem.attrib.clear()
    uselesses = []
    for elem in secelem:
        if elem.tag == 'para':
            texify_para(elem)
        elif elem.tag == 'float':
            texify(elem, float_text(elem))
        elif elem.tag  == 'title': # in ('title', 'subtitle'):
            secelem.set(elem.tag, get_ttn(elem))
            uselesses.append(elem)
        elif elem.tag in ('subsection', 'subparagraph', 'theorem', 'proof', 'paragraph', 'subsubsection'):
            clean_section(elem)
        elif elem.tag == 'note': 
            texify(elem, p_text(elem))
        # elif elem.tag in ('acknowledgements', 'bibliography'):
        #     elem.clear()
        else:
            uselesses.append(elem)
    
    for useless in uselesses:
        secelem.remove(useless)

def clean_chapter(chapelem):
    title = None
    for elem in chapelem:
        if elem.tag == 'para':
            texify_para(elem)
        elif elem.tag == 'toctitle':
            title = p_text(elem)
        elif elem.tag in ('subsection', 'subparagraph', 'section', 'subsubsection'):
            clean_section(elem)
            elem.tag = 'section'
    chapelem.attrib.clear()
    if title:
        chapelem.set('title', title)
    
def texify_abstract(ab):
    '''
    Collect the text at the beginning, within subelements and their trailing to ``txt``,
    clear the element,
    and finally, set the text to ``txt``.
    
    Useful children: p, description, quote, inline-para, section, itemize
    '''
    txt = opening(ab)
    for elem in ab:
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

def bib_text(bib):
    txt = ''
    for elem in bib.iter():
        if elem.tag == 'bibblock':
            txt += ' ' + p_text(elem)
        elif elem.tag == 'para':
            texify_para(elem)
            txt += ' ' + elem.text
    bib.clear()
    bib.text = txt

def clean(root):
    toremove = []
    for child in root:
        if child.tag in ('title', 'subtitle', 'keywords', 'note', 'acknowledgements', 'classification', 'date'):
            # itertext with skipping subelements
            texify(child, p_text(child)) 
        elif child.tag == 'abstract':
            texify_abstract(child)
        elif child.tag in ('section', 'paragraph', 'subparagraph', 'subsection', 'appendix', 'theorem', 'proof'):
            clean_section(child)
            if child.tag not in ('appendix', 'theorem', 'proof'):
                child.tag = 'section'
            if child.get('title', None) == 'abstract':
                child.tag = 'abstract'
        elif child.tag in ('para', 'creator', 'glossarydefinition'): 
            # Collect text with skipping subsubelements
            texify_para(child) 
        elif child.tag == 'titlepage':
            texify_para(child)
        elif child.tag in ('chapter', 'part'):
            clean_chapter(child)
            child.tag = 'chapter'
        elif child.tag == 'bibliography':
            texify(child, bib_text(child))
        else: # Remove <figure>, <float> <table>, <ERROR>, <TOC>, <pagination>, <rdf>, <tags>, <index>, <toctitle>
            toremove.append(child)
    for i in toremove:
        root.remove(i)
    
        
def postcheck(root, errlog):
    skip = False
    secdict = {'abstract': root.findall('abstract'), 'secs':root.findall('section')}
    for title in secdict:
        seclst = secdict[title]
        if len(seclst) == 0: # If there is no such a node
            skip = True
        for sec in seclst:
            if sec.itertext()==None or ''.join(sec.itertext()) == '': # If the section is empty
                skip = True
        if skip:
                print(title + ' absent: ' + xmlpath)
                errlog.write(xmlpath + ' \n' + title + ' absent' + '\n ================================== \n')
    if not skip:
        errlog.write(xmlpath + ' \n' + 'OK' + '\n ================================== \n')
    return skip
            
def get_root(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    ignore_ns(root)
    return tree, root

if __name__ == "__main__":
    # hep-ph0001047.xml
    # tree = ET.parse(join(data_path, 'out.xml'))
    # XXX:subparagraph case: =hep-th0002024.xml
    xmls = [fn for fn in listdir(rawxmls_path) if fn[-4:] == '.xml']
    # xmls = ['=1701.00077.xml']
    with open(cleanlog_path, 'w') as cleanlog:
        for xml in xmls:
            xmlpath = join(rawxmls_path, xml)
            try:
                tree, root = get_root(xmlpath)
            except ET.ParseError:
                print('Skipped: ParseError at %s' % xmlpath)
                cleanlog.write(xmlpath + ' \n' + 'xml.etree ParseError \n' + '================================== \n')
                continue
            clean(root)
            if not postcheck(root, cleanlog):
                tree.write(join(cleanedxml_path, xml))
                # tree.write(join(results_path, 'bib.xml'))
    
