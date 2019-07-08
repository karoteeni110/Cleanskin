from paths import results_path
from os.path import join
from os import listdir
import xml.etree.ElementTree as ET

def get_rank1(rootdir, report=False, node=None):
    rank1 = []
    for fn in listdir(rootdir):
        fpath = join(rootdir, fn)
        if fn[-3:] == 'xml': 
            try:
                tree = ET.parse(fpath)
                root = tree.getroot()
                elemlst = [elem.tag[elem.tag.find('}')+1:] for elem in list(root)]
                rank1.extend(elemlst)
            except ET.ParseError:
                print('ParseError at',fpath)
                continue
        if report:
            if node in set(elemlst):
                print('Found node %s in %s' % (node, fpath))
    return set(rank1)


if __name__ == "__main__":
    travdir = join(results_path, 'latexml/0002')
    # print(get_rank1(travdir))
    get_rank1(travdir, True, 'subparagraph')
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