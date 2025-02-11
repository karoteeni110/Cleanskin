from paths import results_path, data_path, no_sec_xml
from newCleaner import ignore_ns, get_root, mv_titles, retag_useless, is_section, removelist, is_empty_str, is_empty_elem
from os.path import join
from os import listdir
import xml.etree.ElementTree as ET
from collections import Counter
from unicodedata import normalize
import pickle, pprint, re
import numpy as np
    
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
    if type(txt) == str:
        normed = normalize('NFKD', txt).strip()
        if is_empty_str(normed):
            normed = None
        return normed

def title_lens(xmlpath):
    try:
        _ , root = get_root(xmlpath)
        retag_useless(root)
        mv_titles(root)

        lengths = []
        for sec in root.findall('.//section'):
            l = sec.get('title', '') # normed_str(sec.get('title', ''))
            if l:
                lengths.append(len(l.split()))
            # if len(l.split()) > 10:
            #     print(xmlpath)
            #     print(l)
        return lengths

    except ET.ParseError:
        return []

def show_boldtxt_in_para(elem, path):
    if elem.tag == 'para' and len(elem)>=1:
        if len(elem[0]) >=1:
            firstelem = elem[0][0]
            if firstelem.tag == 'text':
                ET.dump(elem)

def all_tags(docroot):
    tagset = []
    for elem in docroot.findall('.//*'):
        tagset.append(elem.tag)
    return tagset

def dp_next_para(present_para, docroot):
    present_para_idx = list(docroot).index(present_para)
    idx = present_para_idx+1
    while docroot[idx].tag != 'para' and idx < len(list(docroot)):
        idx+=1
    if docroot[idx].tag == 'para':
        ET.dump(docroot[idx])
    else:
        print('NO NEXT PARA')


def infer_boldtext(xmlpath):
    try:
        _ , docroot = get_root(xmlpath)
        # retag_useless(docroot)
        retag_useless(docroot)
        mv_titles(docroot)

        paras = docroot.findall("./para/p[1]/text[1]/../..")
        # paras = docroot.findall('./para/p[1]/emph[1]/../..')


        for para in paras:
            elem_p = para.find('p')
            elem_text = elem_p.find('text') # or  # first <p>, first <text>
            # elem_text = elem_p.find('emph')

            elem_text.text = normed_str(elem_text.text)
            elem_text.tail = normed_str(elem_text.tail)

            if elem_text.text:
                intropt = r'((\W)?(1|0|i+|vi{0,4}|iv)?(\W)*?introduction)'
                abspt = r'abstract'
                if elem_p.text == None and 'introduction' in elem_text.text.lower():# re.match(intropt, elem_text.text, flags=re.I):
                    # if len(normed_str(''.join(elem_p.itertext()))) >= 15:
                    if len(elem_text.text.split()) > 1 and len(para.findall('p'))==1:
                        # print(xmlpath)
                        print(elem_text.text)
                        # ET.dump(para)
                        return True


    except ET.ParseError:
        pass

def trav_xmls(rootdir):
    # titlelengths = []
    # xmlcounter = 0
    for i, xml in enumerate(listdir(rootdir)):
        if xml[-3:] == 'xml':
            xmlpath = join(rootdir, xml)
            # try:
            #     _ , root = get_root(xmlpath)
            # titlelengths.extend(title_lens(xmlpath))
            infer_boldtext(xmlpath)
            # except ET.ParseError:

            #     continue

            
            # show_text_starting_paras(xmlpath)
    
        if i % 100 == 0:
            print(i, 'of', len(listdir(rootdir)), '...')
    # titlelengths = np.array(titlelengths)
    # print('%s xmls have tails on intro' % xmlcounter)
    # print('Percentage of titles that is of length shorter than 8:', titlelengths[titlelengths<=8].shape[0] / titlelengths.shape[0] )
    # print('avg title length:', np.mean(titlelengths))
    # print('std:', np.std(titlelengths))
if __name__ == "__main__":
    rootdir = join(results_path, 'no_sec_xml')
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


    # avg title length (words): 3.14261219941 ; std: 2.54380398459 
    # avg title length (chars): 24.3376484204 ; std: 16.4747358315 
    # Percentage of titles with length shorter than 8: 0.95962107248489

    # tag full set:
    # {'backmatter', 'bibrefphrase', 'dots', 'rect', 'polygon', 
    # 'stop', 'XMText', 'table', 'clipPath', 'g', 'bibref', 'subsection', 
    # 'tfoot', 'bibliography', 'index', 'symbol', 'picture', 'creator', 
    # 'bib-related', 'XMHint', 'tags', 'tbody', 'contact', 'acknowledgements', '
    # glossarydefinition', 'break', 'rule', 'inline-block', 'bib-identifier', 
    # 'switch', 'biblist', 'classification', 'bib-title', 'keywords', 'sup', 
    # 'foreignObject', 'bibentry', 'ERROR', 'XMRef', 'MathFork', 'date', 'listingline', 
    # 'equation', 'itemize', 'toctitle', 'line', 'bib-language', 'svg', 'caption', 
    # 'anchor', 'theorem', 'indexmark', 'toccaption', 'XMDual', 'description', 'figure', 
    # 'XMCell', 'resource', 'MathBranch', 'title', 'bezier', 'circle', 'para', 
    # 'linearGradient', 'appendix', 'emph', 'chapter', 'defs', 'enumerate', 
    # 'verbatim', 'pagination', 'td', 'tabular', 'listing', 'bib-data', 'bib-part', 
    # 'inline-para', 'XMWrap', 'bib-note', 'item', 'XMApp', 'indexphrase', 'inline-enumerate', 'bib-publisher', 'radialGradient', 'bibblock', 'thead', 'bib-review', 'personname', 'quote', 'block', 'pattern', 'text', 'subparagraph', 'cite', 'bib-status', 'tr', 'TOC', 'float', 'proof', 'bib-edition', 'equationgroup', 'givenname', 'graphics', 'XMArray', 'ref', 'subsubsection', 'subtitle', 'note', 'XMath', 'part', 'titlepage', 'bib-name', 'bib-links', 'bib-date', 'bibitem', 'inline-item', 'section', 'rdf', 'path', 
    # 'abstract', 'surname', 'tag', 'Math', 'bib-url', 'XMArg', 'paragraph', 'glossaryref', 'use', 'p', 'XMRow', 'XMTok', 'glossaryphrase', 'sub'}
    
    # RANK 1
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


    # <text> fonts:
    # {'slanted', 'sansserif', 'caligraphic', 'italic', 'smallcaps', 'normal', 'bold italic', 'bold smallcaps', 'typewriter', 'bold', 'bold slanted'}

    # [('bold', 745), (None, 369), ('italic', 273), ('slanted', 48), ('smallcaps', 38), ('sansserif', 19), ('typewriter', 13), ('normal', 4), ('bold italic', 3), ('bold smallcaps', 1), ('bold slanted', 1)]

    