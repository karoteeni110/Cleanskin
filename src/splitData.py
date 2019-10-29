from kldiv import read_data, get_pid2cate_dict
from paths import fulltext_dir
from shutil import copy
from os import listdir
from random import choice


def extract_by_cate():
    pass

if __name__ == "__main__":
    cs_paper_pids = [i[:-4] for i in listdir(fulltext_dir) if i[:-3]=='txt']
    pid2cate = get_pid2cate_dict(random_cate=True)
    # pid2cate[pid] = choice([c[3:] 
        #     for c in pid2meta[pid]['categories'].split(', ') 
        #         if c[:2]=='cs'])