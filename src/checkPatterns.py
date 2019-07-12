from paths import results_path, data_path
from xmlCleaner import ignore_ns
from os.path import join
from os import listdir
import xml.etree.ElementTree as ET
from collections import Counter
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
            

def check_childrentags(parent_tag, fpath):
    '''
    Returns the frozenset of all the tags of nodes that are the direct children 
    of nodes with tag ``parent_tag``.


    '''
   
    try:
        tree = ET.parse(fpath)
        root = tree.getroot()
        ignore_ns(root) # get rid of namespace
        direct_children_tags = [child.tag for child in root.findall('./%s/*' % parent_tag)] 
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

# def diff_childtags(elem1, elem2):

if __name__ == "__main__":
    rootdir = join(results_path, 'latexml')
    # pklpath = join(data_path, '1stnodes.pkl')
    # rank1tags_freqdist = get_rank1tags_freqdist(rootdir, oldpkl=pklpath)
    # show_most_common(rank1tags_freqdist, 20)
    # 200 ['resource', 'bibliography', 'title', 'abstract', 'creator', 'section']
    # 136 ['para', 'resource', 'title', 'abstract', 'creator', 'section', 'ERROR']
    # 125 ['resource', 'bibliography', 'title', 'abstract', 'creator', 'date', 'section']
    # 124 ['para', 'resource', 'bibliography', 'title', 'figure', 'abstract', 'creator', 'date', 'classification']

    show_examplefile(rootdir, 'abstract/section')
    
    elemname = 'abstract'
    fd_pkl = join(data_path, '%sTopChildren.pkl' % elemname)
    freqdist = get_childrentag_freqdist(rootdir, elemname, oldpkl=fd_pkl)
    # show_most_common(freqdist, 20)
    # print(all_childtags(freqdist))



    # elemname = 'section'
    # fd_pkl = join(data_path, '%sChildren.pkl' % elemname)
    # section = get_childrentag_freqdist(rootdir, elemname, oldpkl=fd_pkl)

    # elemname = 'paragraph'
    # fd_pkl = join(data_path, '%sChildren.pkl' % elemname)
    # paragraph = get_childrentag_freqdist(rootdir, elemname, oldpkl=fd_pkl)
    # print(all_childtags(section) - all_childtags(paragraph))
    



    # 1701:
    # ParseError at =1701.01158.xml
    # ParseError at =1701.00987.xml

    # RANK 1:
    # {'paragraph', 'tags', 'section', 'subtitle', 'titlepage', 'keywords', 'abstract', 'pagination', 'title', 'TOC', 'note', 'toctitle', 'subsubsection', 'ERROR', 'float', 'subparagraph', 'index', 'classification', 'table', 'appendix', 'date', 'rdf', 'bibliography', 'glossarydefinition', 'chapter', 'proof', 'resource', 'figure', 'creator', 'para', 'subsection', 'acknowledgements', 'theorem'}

    # {'paragraph', 'tags', 'section', 'subtitle', 'titlepage', 'keywords', 
    # 'abstract', 'pagination', 'title', 'TOC', 'note', 'toctitle', 'subsubsection', 
    # 'ERROR', 'float', 'subparagraph', 'index', 'classification', 'table', 'appendix', 
    # 'date', 'rdf', 'bibliography', 'glossarydefinition', 'chapter', 'proof', 
    # 'resource', 'figure', 'creator', 'para', 'subsection', 'acknowledgements', 'theorem'}