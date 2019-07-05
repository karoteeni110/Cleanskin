from subprocess import run, PIPE
from shutil import copyfile, copytree, rmtree
from os import walk, mkdir, stat, remove, listdir
from os.path import basename, dirname, exists, join
from paths import data0001, data0002, data1701, results_path
import time

def latexml(from_fpath, to_fpath):
    a = run('latexml --destination=%s\
        --noparse --nocomments --quiet\
        %s 2>&1' % (to_fpath, from_fpath), shell=True, stdout=PIPE)
    return a

def pick_toptex(artdir):
    a = run('if cd %s ;then ls -hS *.{tex,ltx}; fi' % artdir,
            shell=True, stdout=PIPE, stderr=PIPE, executable='/bin/bash')
    out, err = a.stdout.decode('utf-8').split('\n')[0], a.stderr.decode('utf-8')
    return [out, err]

def trav_data(rootdir, errlog, excluded_arts):
    artdirs = listdir(rootdir)
    ct = 0
    for art in artdirs:
        if art[-1].isdigit() and art not in excluded_arts: # the folder name of articles should consist of digits
            art_path = join(rootdir, art)
            toptex_fn, toptex_err = pick_toptex(art_path)
            toptex_path = join(art_path, toptex_fn)
            output_path = join(results_path, 'latexml/0001/%s.xml' % art)
            if toptex_fn != '': 
                print(art)
                latexml(toptex_path, output_path)
            else:
                errlog.write(art_path + '\n' + toptex_err)
                errlog.write('================================== \n')

        else:
            ct+=1
            print('Skipped art %s of %s' % (ct, len(excluded_arts)))

if __name__ == "__main__":
    errlogpath = join(results_path, 'latexmlLOG.txt')
    rootdir = data0001
    excluded_arts = [i[:-4] for i in listdir(join(results_path,'latexml/0001'))] + ['=hep-ex0001041']
    
    start = time.time()
    with open(errlogpath, 'a') as errlog:
        trav_data(rootdir, errlog, excluded_arts)            
    end = (time.time() - start)/3600
    print('Used time: %s hs' % end)

    # 1701: (354+35) 389/414 files
    # Used time: 118.20650404294332 mins