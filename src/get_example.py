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
    

def get_rank1tags_freqdist(rootdir=None, report_every=100, newpkl=None, oldpkl=None):
    '''
    Collect all the possible direct children of <document>.
    '''
    if not oldpkl:
        nodesetlst = []
        print('Collecting doc infos....')
        for i, fn in enumerate(listdir(rootdir)):
            fpath = join(rootdir, fn)
            if fn[-3:] == 'xml': 
                nodesetlst.append(get_rank1tags(fpath))
            if (i+1) % report_every == 0:
                print('%s of %s collected.' % (i+1, len(listdir(rootdir))))
        rank1nodes = Counter(nodesetlst)
        if newpkl:
            with open(newpkl, 'wb') as f:
                pickle.dump(rank1nodes, f)
    else:
        rank1nodes = pickle.load(open(oldpkl, 'rb'))
    return rank1nodes
    
def show_most_common(counterdict, first):
    for st, ct in counterdict.most_common(first):
        print(ct, list(st))

def show_examplefile(rootdir, tagname):
    '''
    Show example files that contain the tags in ``tagname``.
    ``tagname`` is part of the XPath parameter of 'findall' function: './_tagname_'
    '''
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
            

def check_childrentags(parent_tag, fpath):
    '''
    Returns the frozenset of all the tags of nodes that are the direct children 
    of nodes with tag ``parent_tag``.
    '''
    try:
        tree = ET.parse(fpath)
        root = tree.getroot()
        ignore_ns(root) # get rid of namespace
        direct_children_tags = [child.tag for child in root.findall('./%s' % parent_tag)] 
        return frozenset(direct_children_tags)
    except ET.ParseError:
        print('ParseError at',fpath)
        return frozenset()
    

def get_childrentag_freqdist(rootdir, parent_tag, report_every=100, newpkl=None, oldpkl=None):
    if not oldpkl:
        nodesetlst = []
        print('Collecting doc infos....')
        for i, fn in enumerate(listdir(rootdir)):
            fpath = join(rootdir, fn)
            if fn[-3:] == 'xml': 
                nodesetlst.append(check_childrentags(parent_tag, fpath))
            if (i+1) % report_every == 0:
                print('%s of %s collected.' % (i+1, len(listdir(rootdir))))
        node_freqdist = Counter(nodesetlst)
        if newpkl:
            with open(newpkl, 'wb') as f:
                pickle.dump(node_freqdist, f)
    else:
        node_freqdist = pickle.load(open(oldpkl, 'rb'))
    return node_freqdist

def all_childtags(freqdist):
    mergeset = set().union(*freqdist)
    return mergeset

def show_elempair_exmp(xmlpath, tag, following_tag, leadtagtext):
    try:
        _ , root = get_root(xmlpath)
        # errs = root.findall('.//ERROR')
        # for err in errs:
        #     if leadtagtext in err.text:
        #         print('Find <%s> in %s' % (err.tag, xmlpath))
        # BFS search pairs 
        following_tags = []
        for i in range(0,len(root)-2):
            elempair = (root[i], root[i+1])
            if elempair[0].tag == tag and leadtagtext in elempair[0].text:
                print('Find <%s> <%s> in %s' % (elempair[0].tag, elempair[1].tag, xmlpath))
                print(elempair[0].text) # , ''.join(elempair[1].itertext()))
                # print()
                # following_tags.append(elempair[1].tag)
        return following_tags 
        #         errortexts.append(elempair[0].text)
        # return errortexts
    except ET.ParseError:
        return 0

def show_text(xmlpath, tag):
    try:
        _ , root = get_root(xmlpath)
        elems = root.findall('.//%s' % tag)
        for elem in elems:
            print('Found %s in %s' % (tag, xmlpath))
            print('<%s>'%tag, elem.attrib)
            print(''.join(elem.itertext()))
        print()
    except ET.ParseError:
        return 0

def BFS_generator(root):
    for subelem in root:
        yield subelem

def normedstr(txt):
    return normalize('NFKD', txt).lower().strip()

def is_introsec(elem):
    if elem.tag == 'section' and \
        normedstr(elem.get('title', '')) in ('1introduction', 'introduction'):
        return True
    return False

def elems_before_1stsec(xmlpath):
    try:
        _ , root = get_root(xmlpath)
        retag_useless(root)
        move_titles(root)

        elems, throwits = [], []
        for elem in root:
            if is_section(elem):
                break
            elif elem.tag == 'throwit':
                throwits.append(elem)
            else:
                elems.append(elem)
        if len(elems) + len(throwits) == len(root):
            return []
        else:
            return elems
        
    except ET.ParseError:
        return []

def show_content(elem):
    print('<%s>'% elem.tag, elem.attrib, normedstr(''.join(elem.itertext()))[:200])

def is_shortpara(elem):
    if len(normedstr(''.join(elem.itertext())).split()) <= 5:
        return True
    return False

def show_boldtxt_in_para(elem):
    if elem.tag == 'para' and len(elem)>=1:
        if len(elem[0]) >=1:
            firstelem = elem[0][0]
            if firstelem.tag == 'text' and firstelem.get('font') == 'bold':
                ET.dump(firstelem)
                print()
                
def show_elemcontent(rootdir):
    for i, xml in enumerate(listdir(rootdir)):
        if xml[-3:] == 'xml':
            xmlpath = join(rootdir, xml)
            
            # _, root = get_root(xmlpath)
            # for note in root.findall('.//note'):
            #     print(xmlpath)
            #     ET.dump(note)

            for elem in elems_before_1stsec(xmlpath):
                # show_content(elem)
                show_boldtxt_in_para(elem)
                # show_elempair_exmp(xmlpath, 'ERROR', 'para', 'submitted')
                # show_text(xmlpath, 'classification')
            # print()
        if i % 100 == 0:
            print(i, 'of', len(listdir(rootdir)), '...')

if __name__ == "__main__":
    rootdir = join(results_path, 'latexml')
    # pklpath = join(results_path, '1stnodes_after.pkl')
    # rank1tags_freqdist = get_rank1tags_freqdist(rootdir, oldpkl=pklpath)
    # show_most_common(rank1tags_freqdist, 20)
    # print(all_childtags(rank1tags_freqdist))
    # show_examplefile(rootdir, '/p')
    
    show_elemcontent(rootdir)
    
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