import xml.etree.ElementTree as ET
import sys
from paths import data_path, results_path
from os.path import join


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
    XXX: Don't do "change while iterating"! 
    
    Flatten root: removes all the 'Math' and 'Cite' node in <text> (i.e. param::root), 
    leaving only text within.
    """
    toberemoved = []
    if root.text:
        txt = [root.text.strip('\n')]
    else:
        txt = []

    for child in root:
        if child.tag in keeplist and child.text:
            txt.append(child.text)
        else:
            toberemoved.append((root, child))
        if child.tail:
            txt.append(child.tail)
    for rt, chi in toberemoved:
        rt.remove(chi)
    return ' '.join(txt)

def p_text(p):
    """
    Captures all the text between <p> and </p> 
    with skipping all intermediate tags except <text>.

    Return the concatenated str.
    """
    if p.text:
        following = [p.text.strip('\n')] # head text
    else:
        following = []
    for child in list(p):
        if child.tag == 'text': # pass list!
            following.append(flatten_text(child))
        if child.tail:
            following.append(child.tail.strip('\n'))
    return ' '.join(following)

def ps_text(ps):
    '''
    Iterating ps (a list of <p> elements), passing them to p_text
    and return a str.
    '''
    pstext = []
    for p in ps:
        pstext.append(p_text(p))
    return ' '.join(pstext)

def para_textify(para):
    '''
    Collect all the <p> between <para> & </para>, 
    and pass <p>s to ps_text(). 
    '''
    if para.text:
        ht = para.text.strip('\n') # head text
    else:
        ht = ''
    ps = [elem for elem in list(para) if elem.tag == 'p'] #...
    para.clear()
    para.text = ht + ps_text(ps)

def paras_text(paras):
    '''
    Returns elem.text for each element in paras list.
    If there are other subelem in elem, flatten it with ``para_texify()``.
    '''
    for elem in paras:
        if len(list(elem)) != 0:
            para_textify(elem)
    return ' '.join([elem.text for elem in paras])

def get_ttn(ttelem):
    '''
    Get title str from title element.
    '''
    return flatten_text(ttelem)

def texify_section(secelem):
    paras = []
    for elem in list(secelem):
        if elem.tag == 'para':
            paras.append(elem)
        elif elem.tag == 'title':
            title = get_ttn(elem)
        elif elem.tag == 'subsection':
            texify_section(elem)
            paras.append(elem)
    secelem.clear()
    secelem.set('title', title)
    secelem.text = paras_text(paras)

if __name__ == "__main__":
    # hep-ph0001047.xml
    tree = ET.parse(join(data_path, 'out.xml'))
    root = tree.getroot()

    ignore_ns(root)

    keep_taglist = ['title', 'abstract', 'section', 'subsection', 'chapter', \
         'paragraph', 'subparagraph', 'para', 'p' ,'note', ]
    useless = []
    for child in root:
        if child.tag == 'abstract':
            # Useful: p
            p = list(child)[0]
            child.clear()
            child.text = p_text(p)
        elif child.tag in ('para', 'paragraph') : 
            # Useful: p
            para_textify(child)
            if not child.text:
                useless.append((root, child))
        elif child.tag == 'section':
            # Useful: title, para, subsection
            texify_section(child)
        else:
            useless.append((root,child))
    
    for par, chi in useless:
        par.remove(chi) 

    tree.write(join(results_path, 'newout.xml'))
    
