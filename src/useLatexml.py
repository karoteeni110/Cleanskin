from subprocess import run, PIPE
from shutil import copyfile, copytree, rmtree
from os import walk, makedirs, stat, remove, listdir
from os.path import basename, dirname, exists, join
from paths import data0001, data0002, data1701, results_path, errcase_path
import time

def latexml(from_fpath, to_fpath):
    a = run('latexml --destination=%s\
        --noparse --nocomments --quiet\
        %s 2>&1' % (to_fpath, from_fpath), shell=True, stdout=PIPE)
    return a

def pick_toptex(artdir):
    a = run('if cd %s ;then ls -hS *.{[tT][eE][xX],[lL][tT][xX]}; fi' % artdir,
            shell=True, stdout=PIPE, stderr=PIPE, executable='/bin/bash')
    out = a.stdout.decode('utf-8').split('\n')[0]
    return out

def trav_data(rootdir, errlog, outdir, excluded_dirs=None):
    '''
    Traverse all article directories in ``rootdir``, 
    getting the largest .tex / .ltx file converted to XMLs with latexml.
    XMLs will be written out in ``outdir``

    If the article:
    a) is in TeX format: 
           ==> processed by latexml (output => /outdir/ )
        or ==> in ``excluded_dirs`` (latexml hangs when processing it): cp to /excluded
    b) not in TeX format: 
    '''
    dirs = listdir(rootdir)
    
    for ith, art in enumerate(dirs):
        art_path = join(rootdir, art)

        if art[-1].isdigit() and art not in excluded_dirs: # the folder name of articles should consist of digits
            toptex_fn = pick_toptex(art_path)
            toptex_path = join(art_path, toptex_fn)
            output_path = join(outdir, '%s.xml' % art) # XXX: CHANGE IT
            
            if toptex_fn != '': 
                if not exists(output_path): # Avoid overwriting
                    print(art + ' --> %s of %s' % (ith+1, len(dirs)))
                    cmd = latexml(toptex_path, output_path)
                    if cmd.stdout != b'':
                        print('latexml err:', art_path)
                        # print(cmd.stdout.decode('utf-8'))
                        errlog.write(art_path + '\n' + cmd.stdout.decode('utf-8'))
                        errlog.write('================================== \n')
                else: # Skip extracted articles
                    print('File exists. Skip %s' % toptex_path)
                    
            else: # Articles that are not in LaTex
                err_art_dest = join(errcase_path, 'notex/%s' % art)
                print('Tex not found. Cp %s to %s' % (art, err_art_dest) )
                makedirs(dirname(err_art_dest), exist_ok=True) # check if parent dir exists
                if not exists(err_art_dest):
                    copytree(art_path, err_art_dest)
        else: # TeX cannot be processed by latexml
            dest0 = join(errcase_path, 'excluded/%s' % art)
            makedirs(dirname(dest0), exist_ok=True) # check if parent dir exists
            if not exists(dest0):
                copytree(art_path, dest0)
            print('Excluded dir %s cp to %s' % (art, dest0))

if __name__ == "__main__":
    errlogpath = join(results_path, 'latexml/logs/log.txt')
    rootdir = data1701 # XXX: CHANGE IT
    outdir = join(results_path, 'latexml')
    excluded_arts = ['=hep-ex0001041', '=astro-ph0001216', '=astro-ph0001480'] + ['=astro-ph0002515'] \
                     + ['=1701.00636', '=1701.00146', '=1701.00177', '=1701.01284', '=1701.00785', '=1701.01161', '=1701.00689']
    
    start = time.time()
    with open(errlogpath, 'a') as errlog:
        trav_data(rootdir, errlog, outdir, excluded_arts)          
    end = (time.time() - start)/3600
    print('Used time: %s hs' % end)


    # 1701: (354+35) 389/414 files
    # Used time: 118.20650404294332 mins

    # 0002: 2364 files
    # Used time: 3.0506901219818325 hs+