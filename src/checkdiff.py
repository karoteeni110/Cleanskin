"""
Check discrepencies of files after and before any step.
"""
from os import walk
from os.path import basename, splitext

def subdir_list(parent):
    subdir_bns = next(walk(parent))[1]
    subdir_bns = [ subdir.strip('=') for subdir in subdir_bns ] # strip '='
    return set(subdir_bns)

def fname_list(p):
    for _, __, files in walk(p):
        x = files
        break # need only the first one in the generator
    x = [ splitext(fn)[0] for fn in x ] # strip extensions
    return set(x)
    
def diff_subdirs(path_for_subdirlist, path_for_fnamelist):
    sl1, sl2 = subdir_list(path_for_subdirlist), fname_list(path_for_fnamelist)
    return sl1.symmetric_difference(sl2)

if __name__ == "__main__":
    print(diff_subdirs('/home/yzan/Desktop/try/0001', '/home/yzan/Desktop/arXiv/0001'))
