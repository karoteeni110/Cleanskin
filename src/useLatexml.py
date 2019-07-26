from subprocess import run, PIPE, TimeoutExpired, CalledProcessError
from shutil import copyfile, copytree, rmtree
from os import walk, makedirs, stat, remove, listdir
from os.path import basename, dirname, exists, join
from paths import data0001, data0002, data1701, results_path, errcase_path
import time

def latexml(from_fpath, to_fpath):
    cmd = 'latexml --destination=%s --noparse --nocomments --quiet %s' % (to_fpath, from_fpath)
    try:
        run(cmd, shell=True, stderr=PIPE, check=True, timeout=120)
    except TimeoutExpired:
        return 'Process too long.'
    except CalledProcessError as e:
        return e.stderr.decode('utf-8')
    

def pick_toptex(artdir):
    a = run('if cd %s ;then ls -hS *.{[tT][eE][xX],[lL][tT][xX]}; fi' % artdir,
            shell=True, stdout=PIPE, stderr=PIPE, executable='/bin/bash')
    out = a.stdout.decode('utf-8').split('\n')[0]
    return out

def copyart(errart_path, dest):
    makedirs(dirname(dest), exist_ok=True) # check if parent dir exists
    if not exists(dest):
        copytree(errart_path, dest)

def trav_data(artdir_path_list, errlog, outdir):
    '''
    Traverse all article directories in ``rootdir``, 
    getting the largest .tex / .ltx file converted to XMLs with latexml.
    XMLs will be written out in ``outdir``

    If the article:
    a) is TeX: 
           ==> processed by latexml (output => /outdir/ )
    b) is not TeX: 
    '''
    
    for ith, art_path in enumerate(artdir_path_list):
        art = basename(art_path)

        if art[-1].isdigit(): # the folder name of articles should consist of digits
            toptex_fn = pick_toptex(art_path)
            toptex_path = join(art_path, toptex_fn)
            output_path = join(outdir, '%s.xml' % art) # XXX: CHANGE IT

            if toptex_fn != '': 
                if not exists(output_path): # Avoid overwriting
                    print(art + ' --> %s of %s' % (ith+1, len(artdir_path_list)))
                    msg = latexml(toptex_path, output_path)
                    if msg != None: # If returns error message: copy data & write log
                        # err_art_dest = join(errcase_path, 'excluded/%s' % art)
                        # copyart(art_path, err_art_dest)
                        print('Err at %s' % art)
                        errlog.write(toptex_path + '\n' + msg)
                        errlog.write('================================== \n')
                else: # Skip extracted articles
                    print('File exists. Skip %s' % toptex_path)
                    
            else: # Articles that are not in LaTeX
                # err_art_dest = join(errcase_path, 'notex/%s' % art)
                # copyart(art_path, err_art_dest)
                errmsg = 'Tex not found.'
                print(errmsg)
                errlog.write(toptex_path + '\n' + errmsg)
                errlog.write('================================== \n')


if __name__ == "__main__":
    errlogpath = join(results_path, 'test_runtime.txt') # join(results_path, 'latexml/logs/log.txt')
    rootdir = data1701 # XXX: CHANGE IT
    artdir_path_list = [join(rootdir, dirname) for dirname in listdir(rootdir)]
    # artdir_path_list = [join(rootdir, '=' + dirname) for dirname in ['1701.00576', '1701.00204', '1701.01046']]
    outdir = join(results_path, 'latexml')
    # excluded_arts = ['=hep-ex0001041', '=astro-ph0001216', '=astro-ph0001480'] \
    #                   + ['=astro-ph0002515', '=hep-th0002028'] \
    #                  + ['=1701.00636', '=1701.00146', '=1701.00177', '=1701.01284', '=1701.00785', \
    #                      '=1701.01161', '=1701.00689', '=1701.00635', '=1701.00763']
    
    start = time.time()
    with open(errlogpath, 'a') as errlog:
        trav_data(artdir_path_list, errlog, outdir)          
    end = (time.time() - start)/3600
    print('Used time: %s hs' % end)


    # 1701: (354+35) 389/414 files
    # Used time: 118.20650404294332 mins

    # 0002: 2364 files
    # Used time: 3.0506901219818325 hs+