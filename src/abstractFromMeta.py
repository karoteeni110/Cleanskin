import xml.etree.ElementTree as ET
from newCleaner import get_root
from paths import metadatas_path
from os import listdir
from os.path import join

def read_metaxml(meta_xmlpath):
    _, root = get_root(meta_xmlpath)
    id2abstract = {}
    for article in root:
        urlid = article.find('url').text.split('/')[-1]
        abstract = article.find('abstract').text
        if urlid not in id2abstract:
            id2abstract[urlid] = abstract
        else:
            print('Repeat article: %s' % urlid)
    return id2abstract

def get_urlid2abstract(metadirpath = metadatas_path):
    id2abstract = {}
    for metaxml in listdir(metadirpath):
        cate_meta_path = join(metadirpath, metaxml)
        cate_id2abstract = read_metaxml(cate_meta_path) 
        id2abstract.update(cate_id2abstract)
    return id2abstract

def fn2urlid(fname):
    return 0

if __name__ == "__main__":
    pass
    