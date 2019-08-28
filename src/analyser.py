from paths import results_path, data_path
from newCleaner import ignore_ns, get_root, move_titles, retag_useless, is_section
from os.path import join
from os import listdir
import xml.etree.ElementTree as ET
from collections import Counter
from unicodedata import normalize
import pickle
    
def get_rank1tags(fpath): 
    rank1nodes = []           
    try:
        tree = ET.parse(fpath)
        root = tree.getroot()
        ignore_ns(root) # get rid of namespace
        elemlst = [elem.tag for elem in root.findall('./*')] 
        rank1nodes.extend(elemlst)
        return frozenset(rank1nodes)
    except ET.ParseError:
        print('ParseError at',fpath)
        return frozenset()
    
def show_most_common(counterdict, first):
    for st, ct in counterdict.most_common(first):
        print(ct, list(st))

def show_examplefile(rootdir, tagname):
    """Show example files that contain the tags in ``tagname``.
    ``tagname`` is part of the XPath parameter of 'findall' function: './_tagname_'"""
    for fn in listdir(rootdir):
        fpath = join(rootdir, fn)
        if fn[-3:] == 'xml':
            try:
                tree = ET.parse(fpath)
                root = tree.getroot()
                ignore_ns(root)
                elem = root.findall('./%s' % tagname)
            except ET.ParseError:
                print('ParseError at',fpath)
                elem = []
        
        if elem != []: 
            print('Found %s in %s' % (tagname, fpath))
            # for i in elem:
            #     if i.text == '\\abstract':
            #         print('Found %s in %s' % (tagname, fpath))  

def all_childtags(freqdist):
    mergeset = set().union(*freqdist)
    return mergeset

def normed_str(txt):
    return normalize('NFKD', txt).lower().strip()

def is_introsec(elem):
    if elem.tag == 'section' and \
        normed_str(elem.get('title', '')) in ('1introduction', 'introduction'):
        return True
    return False

def get_upperstream(idx, parent):
    if idx == 0:
        return parent
    

def cut_useless(root):
    retag_useless(root)
    toremove = []
    for p in root.findall('.//throwit/..'):
        for idx, elem in enumerate(p):
            if elem.tag == 'throwit':
                toremove.append((p, elem))
                upper_stream = get_upperstream(idx, p)
                upper_stream.text += elem.text
        # merge its text to the upper non-throwit sibling; if no sbling, then to parent

def show_text_starting_paras(xmlpath):
    try:
        _ , root = get_root(xmlpath)
        retag_useless(root)
        move_titles(root)
        print(xmlpath)

        for text in root.findall(".//para/p[1][text='']/text[1]/.."):
            ET.dump(text)
            print()
        # for elem in root:
        #     if elem.tag == 'para' and len(elem)>=1:
        #         if elem[0].tag =='p' and len(elem[0])>=1:
        #             if elem[0][0] == 'text':
        #                 ET.dump(elem)
    except ET.ParseError:
        pass

def show_content(elem):
    print('<%s>'% elem.tag, elem.attrib, normed_str(''.join(elem.itertext()))[:200])

def is_shortpara(elem):
    if len(normed_str(''.join(elem.itertext())).split()) <= 5:
        return True
    return False

def show_boldtxt_in_para(elem, path):
    if elem.tag == 'para' and len(elem)>=1:
        if len(elem[0]) >=1:
            firstelem = elem[0][0]
            if firstelem.tag == 'text':
                ET.dump(elem)

def all_tags(docroot):
    tagset = []
    for elem in root.findall('./*'):
        tagset.append(elem.tag)
    return tagset


def trav_xmls(rootdir):
    tagset = []
    for i, xml in enumerate(listdir(rootdir)):
        if xml[-3:] == 'xml':
            xmlpath = join(rootdir, xml)
            tagset.extend(all_tags(root))
            # show_text_starting_paras(xmlpath)

    
        if i % 100 == 0:
            print(i, 'of', len(listdir(rootdir)), '...')
    print(set(tagset))
if __name__ == "__main__":
    rootdir = join(results_path, 'latexml')
    # pklpath = join(results_path, '1stnodes_after.pkl')
    # rank1tags_freqdist = get_rank1tags_freqdist(rootdir, oldpkl=pklpath)
    # show_most_common(rank1tags_freqdist, 20)
    # print(all_childtags(rank1tags_freqdist))
    # show_examplefile(rootdir, '/p')
    
    trav_xmls(rootdir)
    
    # elemname = '/note'
    # fd_pkl = join(results_path, 'allnote.pkl')
    # freqdist = get_childrentag_freqdist(rootdir, elemname, newpkl=fd_pkl)
    # show_most_common(freqdist, 20)
    # print(all_childtags(freqdist))





    # RANK 1:
    # {'paragraph', 'tags', 'section', 'subtitle', 'titlepage', 'keywords', 'abstract', 'pagination', 'title', 'TOC', 'note', 'toctitle', 'subsubsection', 'ERROR', 'float', 'subparagraph', 'index', 'classification', 'table', 'appendix', 'date', 'rdf', 'bibliography', 'glossarydefinition', 'chapter', 'proof', 'resource', 'figure', 'creator', 'para', 'subsection', 'acknowledgements', 'theorem'}

    # {'paragraph', 'tags', 'section', 'subtitle', 'titlepage', 'keywords', 
    # 'abstract', 'pagination', 'title', 'TOC', 'note', 'toctitle', 'subsubsection', 
    # 'ERROR', 'float', 'subparagraph', 'index', 'classification', 'table', 'appendix', 
    # 'date', 'rdf', 'bibliography', 'glossarydefinition', 'chapter', 'proof', 
    # 'resource', 'figure', 'creator', 'para', 'subsection', 'acknowledgements', 'theorem'}

    # <ERROR> text:
    # ('\\affil', 98), ('\\abstracts', 90), ('\\address', 77), ('\\refb', 67), ('\\section', 47), 
    # ('\\keywords', 30), ('\\submitted', 23), ('\\reference', 22), ('\\subsection', 22), ('\\thesaurus', 21), 
    # ('\\epsfile', 21), ('\\heading', 17), ('\\sectionb', 15), ('\\recdate', 15), ('\\offprints', 14), 
    # ('\\proof', 12), ('{keywords}', 10), ('\\journalname', 10), ('\\Section', 9), ('\\altaffiltext', 9), 
    # ('\\subtitle', 9), ('\\numberofauthors', 8), ('\\beginfigure', 8), ('\\corollary', 8), ('\\chapter', 7), 
    # ('\\theorem', 7), ('\\figcaption', 7), ('\\+', 6), ('\\articletitle', 6), ('\\name', 6), ('\\begintable', 6), 
    # ('\\proposition', 6), ('\\preprintnumber', 5), ('\\fulladdresses', 5), ('\\wocname', 5), ('\\xyoption', 5), 
    # ('\\newdir', 4), ('\\ignore', 4), ('\\KeyWords', 4), ('\\lefthead', 4), ('\\evenpagefooter', 4), ('\\newarrow', 4), 
    # ('\\@maketitle', 4), ('\\authorrunninghead', 4), ('\\SubSection', 4), ('\\example', 4), ('\\algorithm', 4), 
    # ('\\subsubsection', 3), ('\\affiliation', 3), ('\\templatetype', 3), ('\\verticaladjustment', 3), 
    # ('\\dropcap', 3), ('\\titlehead', 3), ('\\titleb', 3), ('\\authorb', 3), ('\\addressb', 3), ('\\submitb', 3), 
    # ('{summary}', 3), ('\\resthead', 3), ('\\newtheorem', 3), ('\\newdefinition', 3), ('{opening}', 3), 
    # ('\\title', 3), ('\\paperauthor', 3), ('\\addbibresource', 3), ('\\primaryclass', 3), ('\\rec', 3), 
    # ('\\checkfont', 3), ('\\HideDisplacementBoxes', 3), ('\\authoremail', 3), ('\\definecolor', 2), 
    # ('{lemma}', 2), ('\\textlineskip', 2), ('\\upharpoonright', 2), ('\\toctitle', 2), ('\\oddsidemargin', 2), 
    # ('\\summary', 2), ('\\woctitle', 2), ('{fmffile}', 2), ('{CJK*}', 2), ('\\bibpunct', 2), 
    # ('\\author', 2), ('\\abstract', 2), ('\\Author', 2), ('\\newproof', 2), ('\\date', 2), 
    # ('\\Abstract', 2), ('\\NewEnviron', 2), ('\\volumenumber', 2), ('\\asciiabstract', 2), 
    # ('\\secondaryclass', 2), ('\\authorinfo', 2), ('\\euro', 2), ('{PACS}', 2), ('\\category', 2), 
    # ('\\terms', 2), ('\\newfloatcommand', 2), ('\\runninghead', 2), ('\\DeclareUnicodeCharacter', 2), ('\\question', 2)

    # <text> fonts:
    # {'slanted', 'sansserif', 'caligraphic', 'italic', 'smallcaps', 'normal', 'bold italic', 'bold smallcaps', 'typewriter', 'bold', 'bold slanted'}

    # [('bold', 745), (None, 369), ('italic', 273), ('slanted', 48), ('smallcaps', 38), ('sansserif', 19), ('typewriter', 13), ('normal', 4), ('bold italic', 3), ('bold smallcaps', 1), ('bold slanted', 1)]