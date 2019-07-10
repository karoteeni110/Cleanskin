from paths import results_path
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
        elemlst = [elem.tag[elem.tag.find('}')+1:] for elem in list(root)] # get rid of namespace
        rank1nodes.extend(elemlst)
    except ET.ParseError:
        print('ParseError at',fpath)
    return frozenset(rank1nodes)

def get_all_rank1(rootdir, report_every=1, dumpnew = True, pkl = None):
    '''
    Collect all the possible direct children of <document>.
    '''
    if not pkl:
        nodesetlst = []
        print('Collecting doc infos....')
        for i, fn in enumerate(listdir(rootdir)):
            fpath = join(rootdir, fn)
            if fn[-3:] == 'xml': 
                nodesetlst.append(get_rank1(fpath))
            if (i+1) % report_every == 0:
                print('File %s of %s collected.' % (i+1, len(listdir(rootdir))))
        rank1nodes = Counter(nodesetlst)
    else:
        reak1nodes = pickle.load(pkl)
            
    # Print out 
    for a in rank1nodes:
        print(rank1nodes[a], list(a))
            


if __name__ == "__main__":
    travdir = join(results_path, 'latexml')
    # print(get_rank1(travdir))
    get_all_rank1(travdir, 50)
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