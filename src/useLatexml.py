from subprocess import run, PIPE
from shutil import copyfile, copytree, rmtree
from os import walk, mkdir, stat, remove, listdir
from os.path import basename, dirname, exists, join
from paths import data0001, data0002, data1701, results_path

def latexml(from_fpath, to_fpath):
    a = run('latexml --destination=%s\
        --noparse --nocomments --quiet\
        %s 2>&1' % (to_fpath, from_fpath), shell=True, stdout=PIPE)
    return a

def pick_toptex(artdir):
    a = run('cd %s | ls -hS *.{tex,ltx}' % artdir,
            shell=True, stdout=PIPE, stderr=PIPE, executable='/bin/bash')
    out, err = a.stdout.decode('utf-8').split('\n')[0], a.stderr.decode('utf-8')
    return [out, err]

def trav_data(rootdir, errlog):
    artdirs = listdir(rootdir)
    for art in artdirs:
        if art[-1].isdigit(): # the folder name of articles should consist of digits
            art_path = join(rootdir, art)
            toptex_fn, toptex_err = pick_toptex(art_path)
            toptex_path = join(art_path, toptex_fn)
            output_path = join(results_path, 'latexml/%s.xml' % art)
            if toptex_fn != '': 
                latexml(toptex_path, output_path)
            else:
                errlog.write(art_path + '\n' + toptex_err)
                errlog.write('==================================')
        else:
            print('You fucked up! hahahahahha')

if __name__ == "__main__":
    errlogpath = join(results_path, 'latexmlLOG.txt')
    rootdir = data1701
    with open(errlogpath, 'a') as errlog:
        trav_data(rootdir, errlog)            