import xml.etree.ElementTree as ET
from paths import metadatas_path
from os import listdir
from os.path import join
import time, re

def url2artid(url):
    urlid = url.split('/')[-2:]
    if urlid[0] == 'abs':
        return urlid[1] # 1701
    else:
        return urlid[0] + urlid[1] # 0001, 0002

def demath(abstract):
    return re.sub(r'\$.*?\$', ' ', abstract, flags=re.M | re.S) # multi-line | dot-match-all

def read_metaxml(meta_xmlpath):
    root = ET.parse(meta_xmlpath).getroot()
    id2meta = {}
    for article in root:
        artid = url2artid(article[5].text)
        abstract, cates = demath(article[3].text), article[-1].text
        id2meta[artid] = {'abstract': abstract, 'categories': cates}
    return id2meta

def get_urlid2meta(metadirpath = metadatas_path):
    id2meta = {}
    begin = time.time()
    print('Reading metadata. Expected time: 1 min')
    for metaxml in listdir(metadirpath): # ['Astrophysics.xml']:
        print('Reading', metaxml, '...')
        cate_meta_path = join(metadirpath, metaxml)
        ith_id2meta = read_metaxml(cate_meta_path) 
        id2meta.update(ith_id2meta)

    end = (time.time() - begin) / 60
    # print('Used time: %s min' % end )
    return id2meta

if __name__ == "__main__":
    print(get_urlid2meta()['astro-ph0001020'])
    