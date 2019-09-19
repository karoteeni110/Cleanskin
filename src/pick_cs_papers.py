import xml.etree.ElementTree as ET
from newCleaner import get_root
from clean_at_tmp import level, format, run_and_report_done
from os import listdir
from paths import 

def is_longtoken_sec(sec):
    """Check if the tokens within `sec` are concatenated:
    If len(text)/len(text.split()) > 10.0, return True ;
    else: False
    """
    return False

def cp_1tar(tarfn):
    pass

def unzip_1tar(tarfn):
    pass

def rm_oldtar(tarfn):
    pass

def pick_cs_papers(tarfn):
    fulltext_dst = 
    pass

def rm_picked_dir(tarfn):
    pass

def main(tar_fn):
    cp_1tar(tar_fn)
    unzip_1tar(tar_fn)
    rm_oldtar(tar_fn)
    pick_cs_papers(tar_fn)
    rm_picked_dir(tar_fn)
    get_topic_probs() 
    # Finally get `cs_ft_composition.txt`, `cs_abt_composition.txt`, `cs_ft_keys.txt`

if __name__ == "__main__":
    tarlist = [fn for fn in listdir('/cs/group/grp-glowacka/arxiv/xml') \
                if fn[-2:] == 'gz' and fn not in listdir('/cs/group/grp-glowacka/arxiv/cleaned_xml')] 

