from newCleaner import *
from subprocess import run, PIPE, CalledProcessError
from shutil import copyfile, copytree, rmtree
from os import listdir, remove
from os.path import join

def run_and_report(msg, cmd):
    try:
        run(cmd, shell=True, stderr=PIPE, check=True)
    except CalledProcessError as e:
        return e.stderr.decode('utf-8')
    else: 
        print(msg)


def cp_1tar(tar_fn):
    src_tarpath = join('/cs/group/grp-glowacka/arxiv/xml', tar_fn)
    dst_tarpath = join('/tmp/arxiv', tar_fn)
    _ = copyfile(src_tarpath, dst_tarpath)

def unzip_1tar(tar_fn):
    cmd = 'tar -xzf %s' % join('/tmp/arxiv', tar_fn)
    

def rm_oldtar(tar_fn):
    remove(join('/tmp/arxiv', tar_fn))
    print('Old tar /tmp/arxiv/%s removed' % tar_fn)

def cleanse(tar_fn):
    pass 

def tarn2dirn(tar_fn):
    return tar_fn[:5]

def tarback(tar_fn):
    cmd = 'tar -czf %s %s/' % (tar_fn, tarn2dirn(tar_fn))  
    run(cmd)

def rm_cleansed_dir(tar_fn):
    pass

def mv_newtar(tar_fn):
    pass

def main(tar_fn):
    cp_1tar(tar_fn)
    unzip_1tar(tar_fn)
    rm_oldtar(tar_fn)
    cleanse(tar_fn)
    tarback(tar_fn)
    rm_cleansed_dir(tar_fn)
    mv_newtar(tar_fn)

if __name__ == "__main__":
    tarlist = [join('/cs/group/grp-glowacka/arxiv/xml', '0001.tar.gz')]
    # tarlist = [fn for fn in listdir('/cs/group/grp-glowacka/arxiv/xml') if fn[-2:] == 'gz']
    for i, tarfn in enumerate(tarlist):
        print('Tarball %s of %s ...', (i+1, len(tarlist)))
        main(tarfn)

