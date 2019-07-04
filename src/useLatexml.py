from subprocess import run, PIPE
from shutil import copyfile, copytree, rmtree
from os import walk, mkdir, stat, remove
from os.path import basename, dirname, exists

def latexml(from_fpath, to_fpath):
    a = run('latexml --destination=%s\
        --noparse --nocomments --quiet\
        %s 2>&1' % (to_fpath, from_fpath), shell=True, stdout=PIPE)
    return a

def check_err(cmd, infile, outfile, errlog, errlogpath):
    if cmd.stdout != b'':
        errlog.write(infile + ' \n' + cmd.stdout.decode('utf-8'))
        errlog.write('========================================= \n')
    
    if exists(outfile):
        if stat(outfile).st_size == 0:
            remove(outfile)
            errlog.write(infile + ' \n' + 'Empty output.')
            errlog.write('========================================= \n')
    else:
        errlog.write(infile + ' \n' + 'Writing failed.')
        errlog.write('========================================= \n')


        


