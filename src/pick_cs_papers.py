import xml.etree.ElementTree as ET
import logging
from newCleaner import get_root
from clean_at_tmp import level, format, run_and_report_done, unzip_1tar, rm_oldtar
from metadata import get_urlid2meta
from shutil import copyfile
from os import listdir
from os.path import join 
from paths import *

handlers = [logging.FileHandler('topicmodel.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)

def is_longtoken_sec(secelem):
    """Check if the tokens within `sec` are concatenated:
    If len(text)/len(text.split()) > 10.0, return True ;
    else: False
    """
    return False

def cp_1tar(tarfn):
    src = join(CLEANED_XML, tarfn)
    dst = join(TMP_ARXIV, tarfn)
    copyfile(src, dst)
    return dst

def pick_cs_papers(tarfn):
    dirn = join(TMP_ARXIV, tarfn)
    for xml in listdir(dirn):
        xmlpath = 
        _, root = get_root()
    pass

def rm_picked_dir(tarfn):
    pass

def get_topic_probs():
    pass

def main(tar_fn):
    cp_1tar(tar_fn)
    unzip_1tar(tar_fn)
    rm_oldtar(tar_fn)
    pick_cs_papers(tar_fn)
    rm_picked_dir(tar_fn)
    get_topic_probs() 
    # Finally get `cs_ft_composition.txt`, `cs_abt_composition.txt`, `cs_ft_keys.txt`



CLEANED_XML = '/cs/group/grp-glowacka/arxiv/cleaned_xml'
TMP_ARXIV = '/tmp/arxiv'

if __name__ == "__main__":
    tarlist = [fn for fn in listdir(CLEANED_XML) \
                if fn not in listdir(cs_lda_dir)] 

    # Set verbose
    VERBOSE, REPORT_EVERY = True, 500

    # Read metadata for all articles
    id2meta = get_urlid2meta() # 1 min

    for i, tarfn in enumerate(tarlist):
        logging.info('Tarball %s of %s ...' % (i+1, len(tarlist)))
        main(tarfn)

