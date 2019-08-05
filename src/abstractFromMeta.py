import xml.etree.ElementTree as ET
from newCleaner import get_root
from paths import metadatas_path
from os import listdir
from os.path import join

def url2artid(url):
    urlid = url.split('/')[-2:]
    if urlid[0] == 'abs':
        return urlid[1]
    else:
        return urlid[0] + urlid[1]

def read_metaxml(meta_xmlpath):
    _, root = get_root(meta_xmlpath)
    id2abstract = {}
    for article in root:
        artid = url2artid(article.find('url').text)
        abstract = article.find('abstract').text
        if artid not in id2abstract:
            id2abstract[artid] = abstract
        else:
            print('Repeat article: %s' % artid)
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
    