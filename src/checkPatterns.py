from paths import results_path, data_path
from xmlCleaner import ignore_ns
from os.path import join
from os import listdir
import xml.etree.ElementTree as ET
from collections import Counter
import pickle
    
def get_rank1(fpath): 
    rank1nodes = []           
    try:
        tree = ET.parse(fpath)
        root = tree.getroot()
        ignore_ns(root)
        elemlst = [elem.tag for elem in root.findall('./*')] # get rid of namespace
        rank1nodes.extend(elemlst)
    except ET.ParseError:
        print('ParseError at',fpath)
    return frozenset(rank1nodes)

def get_all_rank1(rootdir=None, report_every=100, newpkl=None, oldpkl=None):
    '''
    Collect all the possible direct children of <document>.
    '''
    if not oldpkl:
        nodesetlst = []
        print('Collecting doc infos....')
        for i, fn in enumerate(listdir(rootdir)):
            fpath = join(rootdir, fn)
            if fn[-3:] == 'xml': 
                nodesetlst.append(get_rank1(fpath))
            if (i+1) % report_every == 0:
                print('File %s of %s collected.' % (i+1, len(listdir(rootdir))))
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

def show_examplefile(rootdir, tagname, rank1only=True):
    '''
    Show example files that contain the tags in ``tagname``.
    '''
    for fn in listdir(rootdir):
        fpath = join(rootdir, fn)
        if fn[-3:] == 'xml':
            try:
                tree = ET.parse(fpath)
                root = tree.getroot()
                ignore_ns(root)
                if rank1only:
                    elem = root.findall(tagname)
                else:
                    elem = root.findall('.//%s'% tagname)
            except ET.ParseError:
                print('ParseError at',fpath)
                elem = []
        
        if elem != []: 
            print('Found %s in %s' % (tagname, fpath))
            

def check_children(parent_tag, fpath):
    direct_children_tags = []           
    try:
        tree = ET.parse(fpath)
        root = tree.getroot()
        ignore_ns(root) # get rid of namespace
        child_taglst = [child.tag for child in root.findall('.//%s/*' % parent_tag)] 
        direct_children_tags.extend(child_taglst)
    except ET.ParseError:
        print('ParseError at',fpath)
    return frozenset(direct_children_tags)

def check_children_iter(rootdir, parent_tag, report_every=100, newpkl=None, oldpkl=None):
    if not oldpkl:
        nodesetlst = []
        print('Collecting doc infos....')
        for i, fn in enumerate(listdir(rootdir)):
            fpath = join(rootdir, fn)
            if fn[-3:] == 'xml': 
                nodesetlst.append(check_children(parent_tag, fpath))
            if (i+1) % report_every == 0:
                print('File %s of %s collected.' % (i+1, len(listdir(rootdir))))
        node_freqdist = Counter(nodesetlst)
        if newpkl:
            with open(newpkl, 'wb') as f:
                pickle.dump(node_freqdist, f)
    else:
        node_freqdist = pickle.load(open(oldpkl, 'rb'))
    return node_freqdist


if __name__ == "__main__":
    rootdir = join(results_path, 'latexml')
    pklpath = join(data_path, '1stnodes.pkl')
    nodes = get_all_rank1(rootdir, oldpkl=pklpath)
    # show_most_common(nodes,20)
    # show_examplefile(rootdir, ['resource', 'abstract', 'section', 'title', 'creator', 'bibliography'])
    # show_examplefile(rootdir, ['para', 'title', 'creator', 'resource', 'ERROR', 'section', 'abstract'])

    # fd_pkl = join(data_path, 'paraChildren.pkl')
    # freqdist = check_children_iter(rootdir, 'para', oldpkl=fd_pkl)
    # show_most_common(freqdist, 20)




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