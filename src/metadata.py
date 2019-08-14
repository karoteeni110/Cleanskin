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

def elem2artid(artelem):
    return url2artid(artelem[5].text)

def demath(abstract):
    return re.sub(r'\$.*?\$', ' ', abstract, flags=re.M | re.S) # multi-line | dot-match-all

def meta_to_add(artelem):
    title = artelem[1].text
    abstract = demath(artelem[3].text)
    categories = artelem[-1].text
    author = artelem[2].text
    return title, abstract, categories, author

def read_metaxml(meta_xmlpath):
    root = ET.parse(meta_xmlpath).getroot()
    id2meta = {}
    for article in root:
        artid = elem2artid(article)
        title, abstract, categories, author = meta_to_add(article)
        id2meta[artid] = {'abstract': abstract, 'categories': categories, 'author': author, 'title': title}
    return id2meta

def get_urlid2meta(metadirpath = metadatas_path):
    id2meta = {}
    begin = time.time()
    print('Reading metadata... It takes about 1 min')
    
    # metaxml_list = listdir(metadirpath)
    metaxml_list = ['Computer_Science.xml']
    for metaxml in metaxml_list: # :
        if metaxml[-3:] == 'xml':
            print('Reading', metaxml, '...')
            cate_meta_path = join(metadirpath, metaxml)
            ith_id2meta = read_metaxml(cate_meta_path) 
            id2meta.update(ith_id2meta)

    end = (time.time() - begin) / 60
    # print('Used time: %s min' % end )
    return id2meta

if __name__ == "__main__":
    print(get_urlid2meta()['astro-ph0001020'])
    