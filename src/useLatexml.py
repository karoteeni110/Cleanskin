from subprocess import run, PIPE, TimeoutExpired, CalledProcessError
from shutil import copyfile, copytree, rmtree
from os import walk, makedirs, stat, remove, listdir
from os.path import basename, dirname, exists, join
# from paths import data0001, data0002, data1701, results_path, errcase_path
import time

def latexml(from_fpath, to_fpath):
    cmd = 'latexml --destination=%s --noparse --nocomments --quiet %s' % (to_fpath, from_fpath)
    try:
        run(cmd, shell=True, stderr=PIPE, check=True, timeout=100)
    except TimeoutExpired:
        return 'Process too long.'
    except CalledProcessError as e:
        return e.stderr.decode('utf-8')

def pick_toptex(artdir):
    """ Return the 
    """
    a = run('if cd %s ;then ls -hS *.{[tT][eE][xX],[lL][tT][xX]}; fi' % artdir,
            shell=True, stdout=PIPE, stderr=PIPE, executable='/bin/bash')
    out = a.stdout.decode('utf-8').split('\n')[0]
    return out

def copyart(errart_path, dest):
    makedirs(dirname(dest), exist_ok=True) # check if parent dir exists
    if not exists(dest):
        copytree(errart_path, dest)

def trav_data(artdir_path_list, outdir, errlogpath=None):
    """params: 
    `artdir_path_list`: a list of paths of articles' directories. E.g. ['../1701/=1701.00003', '../1701.00078']
    `errlogpath`: the path of error log; default None
    `outdir`: the destination directory for the XML outputs. 
    So the .xml files will be write out to 'outdir/article_id.xml' (`article_id` comes from the basename of `artdir_path`)

    Traverse all article directories in ``rootdir``, 
    find the largest .tex/.ltx in the article directory and convert it to XML.
    XMLs will be written out in ``outdir``

    If the article:
    a) has a top .tex file: 
           ==> process b latexml
    b) doesn't have a tex:
           ==> print `TeX not found` + error message
    """
    if errlogpath:
        errlog = open(errlogpath, 'a')
    else:
        errlog = False

    for ith, art_path in enumerate(artdir_path_list):
        art = basename(art_path)

        if art[-1].isdigit(): # the folder name of articles should consist of digits
            toptex_fn = pick_toptex(art_path)
            toptex_path = join(art_path, toptex_fn)
            output_path = join(outdir, '%s.xml' % art) 

            if toptex_fn != '': 
                if not exists(output_path): # Avoid overwriting
                    print(art + ' --> %s of %s' % (ith+1, len(artdir_path_list)))
                    msg = latexml(toptex_path, output_path)
                    if msg != None: 
                        print('Error at %s' % art)
                        if errlog:
                            errlog.write(toptex_path + '\n' + msg)
                            errlog.write('================================== \n')
                else: # Skip extracted articles
                    print('File exists. Skip %s' % toptex_path)
                    
            else: # Articles that are not in LaTeX
                # err_art_dest = join(errcase_path, 'notex/%s' % art)
                # copyart(art_path, err_art_dest)
                errmsg = 'Tex not found.'
                print(errmsg)
                if errlog:
                    errlog.write(toptex_path + '\n' + errmsg)
                    errlog.write('================================== \n')
    if errlog:
        errlog.close()

if __name__ == "__main__":
    """Params:
    `errlogpath`: the path of error log. 
    `rootdir`: the path of the directory where the article folders are
    `outdir`: the destination directory of xmls
    """
    # Change parameters here
    errlogpath = join('/home/yzan/Desktop/try/cluster/1701try', 'error_log.txt') 
    rootdir = '/home/yzan/Desktop/try/cluster/1701try' 
    outdir = join('/home/yzan/Desktop/try/cluster', 'latexml') 
    

    # === Don't touch ===
    artdir_path_list = [join(rootdir, dirname) for dirname in listdir(rootdir)]
    start = time.time()
    trav_data(artdir_path_list, outdir)          
    end = (time.time() - start)/60
    print('Used time: %s mins' % end)


    # 1701: (354+35) 389/414 files
    # Used time: 118.20650404294332 mins

    # 0002: 2364 files
    # Used time: 3.0506901219818325 hs