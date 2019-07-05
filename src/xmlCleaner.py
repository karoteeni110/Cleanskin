import xml.etree.ElementTree as ET
import sys
from paths import data_path, results_path
from os.path import join


def ignore_ns(root):
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

def clean_by_tag(root, keeplist):
    """
    XXX: Don't do "change while iterating"! 
    https://stackoverflow.com/questions/22817530/elementtree-element-remove-jumping-iteration
    
    Removes only the **direct** child elements on the root.
    """
    toberemoved = []
    for child in root:
        if child.tag in keeplist:
            print(child.tag, child.attrib)
            print([ (ele.tag, ele.attrib) for ele in list(child)])
            print('========================')
    #     if child.tag not in keeplist:
    #         toberemoved.append(child)
    # for elem in toberemoved:
    #     root.remove(elem)

def iter_clean(docroot, keeplist):
    """
    Use `clean_by_tag` iteratively.
    """
    for elem in docroot.iter():
        clean_by_tag(elem, keeplist)

def p_text(p):
    """
    Captures all the text between <p> and </p> 
    with skipping all intermediate tags.

    Return the concatenated str.
    """
    following = [p.text.strip('\n')] # head text
    for math in list(p):
        following.append(math.tail.strip('\n')) # following text
    return ''.join(following)

def ps_text(ps):
    pstext = []
    for p in ps:
        pstext.append(p_text(p))
    return ' '.join(pstext)

def para_textify(para):
    ps = [elem for elem in list(para) if elem.tag == 'p'] #...
    para.clear()
    para.text = ps_text(ps)

def paras_text(paras):
    parastext = []
    for para in paras:
        parastext.append(para.text)
    return ' '.join(paras_text)

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

        elif child.tag == 'para' : 
            # Useful: p
            para_textify(child)

        elif child.tag == 'section':
            # Useful: title, para
            paras = []
            for elem in list(child):
                if elem.tag == 'para':
                    paras.append(elem)
                elif elem.tag == 'title':
                    title = elem
                else:
                    useless.append((child, elem))
            child.clear()
            child.text = paras_text(paras)
        
        else:
            useless.append((root,child))
    
    for par, chi in useless:
        par.remove(chi)



    # iter_clean(root, keep_taglist)
    tree.write(join(results_path, 'newout.xml'))
    
