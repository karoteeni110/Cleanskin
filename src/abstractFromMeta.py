import xml.etree.ElementTree as ET
from paths import metadatas_path
from os import listdir
from os.path import join
import time

def url2artid(url):
    urlid = url.split('/')[-2:]
    if urlid[0] == 'abs':
        return urlid[1] # 1701
    else:
        return urlid[0] + urlid[1] # 0001, 0002

def read_metaxml(meta_xmlpath):
    root = ET.parse(meta_xmlpath).getroot()
    id2abstract = {}
    for article in root:
        artid = url2artid(article[5].text)
        abstract = article[3].text
        id2abstract[artid] = abstract
    return id2abstract

def get_urlid2abstract(metadirpath = metadatas_path):
    id2abstract = {}
    begin = time.time()
    for metaxml in listdir(metadirpath):
        print('Reading', metaxml, '...')
        cate_meta_path = join(metadirpath, metaxml)
        cate_id2abstract = read_metaxml(cate_meta_path) 
        id2abstract.update(cate_id2abstract)
    end = (time.time() - begin) / 60
    print('Used time: %s min' % end )
    return id2abstract

if __name__ == "__main__":
    print(get_urlid2abstract()['astro-ph0001020'])
    