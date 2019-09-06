from paths import results_path, data_path
from newCleaner import ignore_ns, get_root, mv_titles, retag_useless, is_section, removelist, is_empty_str
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

def get_upstream(idx, parent):
    if idx == 0:
        return parent
    else:
        previous_ele_idx = idx-1
        while parent[previous_ele_idx].text == None or parent[previous_ele_idx].tag == 'throwit' and previous_ele_idx > 0:
            previous_ele_idx -= 1
        return parent[previous_ele_idx]

def cut_useless(root):
    retag_useless(root)
    toremove = []
    for p in root.findall('.//throwit/..'):
        for idx, elem in enumerate(p):
            if elem.tag == 'throwit':
                toremove.append((p, elem))
                if elem.text:
                    upstream = get_upstream(idx, p)
                    if upstream.tail:
                        try:
                            upstream.text += ' ' + normed_str(upstream.tail)
                        except TypeError:
                            upstream.text = normed_str(upstream.tail)
                        upstream.tail = None
                    try:
                        upstream.text += ' ' + normed_str(elem.text)
                    except TypeError:
                        upstream.text = normed_str(elem.text)

                    elem.text = None
    for p,c in toremove:
        p.remove(c)
        # merge its text to the upper non-throwit sibling; if no sbling, then to parent

def title_lens(xmlpath):
    try:
        _ , root = get_root(xmlpath)
        retag_useless(root)
        mv_titles(root)

        lengths = []
        for sec in root.findall('.//section'):
            l = normed_str(sec.get('title', ''))
            if l:
                lengths.append(len(l))
                if len(l)<=4:
                    print(xmlpath)
                    print('short title:', sec.get('title')) 
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


def infer_boldtext(xmlpath):
    try:
        _ , docroot = get_root(xmlpath)
        # retag_useless(docroot)
        cut_useless(docroot)
        mv_titles(docroot)

        paras = docroot.findall("./para/p[1]/text[1]/../..")

        for para in paras:
            elem_p = para.find('p')
            elem_text = elem_p.find('text') # first <p>, first <text>

            elem_text.text = normed_str(elem_text.text)
            elem_text.tail = normed_str(elem_text.tail)
            if elem_text.text:
                intropt = r'((i+\W|vi{0,4}\W|iv\W)?\bintroduction)'
                abspt = r'abstract'
                if elem_p.text == None and re.match(abspt, elem_text.text, flags=re.I): #and len(para) == len(elem_p) == 1:
                    # para_idx = list(docroot).index(para)
                    # ET.dump(elem_text) # in tail or its child
                    # print('Yes')
                    if len(elem_text.text) > 10:
                        pass

                    elif elem_text.tail: # abstract within <text>
                        if len(elem_text.tail) > 10:
                            print(xmlpath)
                            ET.dump(elem_p)
                            print()

                    # if not elem_text.tail:
                    #     # in its child
                    #     if len(elem_text) >=10:
                    #         pass
                    #     # content in next para:
                    #     try:
                    #         next_para_idx = para_idx+1
                    #         while docroot[next_para_idx].tag != 'para' or normed_str(''.join(docroot[next_para_idx].itertext())) == '':
                    #             next_para_idx += 1
                    #         print('Next para:')
                    #         ET.dump(docroot[next_para_idx])
                    #         # pp = pprint.PrettyPrinter(indent=4)
                    #         # pp.pprint('next para text (normed):' + '[' + ''.join(docroot[next_para_idx].itertext()) +']')

                    #         # content in its child:

                    #         # in sibling:
                    #     except IndexError:
                    #         print('No next para')
                    # print()


    except ET.ParseError:
        pass

def trav_xmls(rootdir):
    # titlelengths = []
    for i, xml in enumerate(listdir(rootdir)):
        if xml[-3:] == 'xml':
            xmlpath = join(rootdir, xml)
            # try:
            #     _ , root = get_root(xmlpath)
            infer_boldtext(xmlpath)
            # except ET.ParseError:
            #     continue

            
            # show_text_starting_paras(xmlpath)
        if i % 100 == 0:
            print(i, 'of', len(listdir(rootdir)), '...')
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

    # avg section title length: 24.3376484204 ; std: 16.4747358315