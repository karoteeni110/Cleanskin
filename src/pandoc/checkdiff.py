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
    diff = sl1.symmetric_difference(sl2)
    print('len(arg2):', len(sl2))
    print('len(arg1):', len(sl1))
    print('Difference: arg2 - arg1 =', len(sl2)-len(sl1))
    print(diff, ' => %d discrepencies' % len(diff))

if __name__ == "__main__":
    dddd = '1701'
    print('Checking %s' % dddd)
    diff_subdirs('/home/yzan/Desktop/try/%s' % dddd, '/home/yzan/Desktop/arXiv/%s' % dddd)
