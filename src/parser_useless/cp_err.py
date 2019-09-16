from shutil import copytree, copy, move
from paths import results_path, errcase_path, data_path
from os.path import basename, join, exists, dirname
from os import listdir


def get_srcpath(logpath):
    with open(logpath, 'r') as log:
        f = log.readlines()
    cplst = []
    for line in f:
        a = line.split()[-1]
        if exists(a):
            src = a
            dest = join(errcase_path, basename(src))
            cplst.append((src, dest))
    for src, dest in set(cplst): # Avoid repeated cp
        print('CP: %s' % src)
        if src[-4:] == '.xml':
            # copy(src, dest)
            artdir = join(data_path, basename(dirname(src)) + '/' + basename(src)[:-4])
            dest = dest[:-4]
            copytree(artdir, dest)
        else:
            copytree(src, dest)

def mv_pdf_artdir(errart, dst):
    """
    Move the directory ``errart`` to ``dst``
    if it contains only files ended with `ps, html, pdf...` etc. 
    """
    fs = listdir(errart)
    ext = [f.split('.')[-1].lower() for f in fs]
    if set(ext) <= set(['ps', 'html', 'pdf', 'eps', 'cry', 'gif', 'jpg','doc', 'htm', 'cls']) \
        or fs[0] == 'withdrawn':
        print('MV %s to %s: no tex' % (errart, dst) )
        move(errart, dst)




if __name__ == "__main__":
    # logpt = join(results_path, 'latexml/outError.txt')
    # get_srcpath(logpt)

    for i in listdir(errcase_path):
        if i[-1].isdigit(): # if ``i`` is directory
            mv_pdf_artdir(join(errcase_path, i), join(errcase_path, 'notex'))
