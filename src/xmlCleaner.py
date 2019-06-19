"""
Rules out the <acknowledgement> and <references> sections.
Flattens the subsections.

Does NOT assume single layer subsection structure.
"""
import xml.etree.ElementTree as ET
from unicodedata import normalize
from os.path import basename, join
from paths import within_results
import sys

fpath = sys.argv[1] # abspath of the xml
if fpath[-4:] != '.xml':
    raise AssertionError ("Not XML!")
data = open(fpath,'r')
tree = ET.parse(data)
root = tree.getroot()

def recur_rm(parent):
    '''Check and remove the acknowledgement sec in the children.
    '''
    for child in list(parent): # If no child, list is empty
        if child.get('text', False).lower() in ('acknowledgements', 'references', 'bibliography'):
            parent.remove(child)
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
    dddd = '0002'
    diff_subdirs('/home/yzan/Desktop/try/%s' % dddd, '/home/yzan/Desktop/arXiv/%s' % dddd)
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
    dddd = '0002'
    diff_subdirs('/home/yzan/Desktop/try/%s' % dddd, '/home/yzan/Desktop/arXiv/%s' % dddd)
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
    dddd = '0002'
    diff_subdirs('/home/yzan/Desktop/try/%s' % dddd, '/home/yzan/Desktop/arXiv/%s' % dddd)tions into one whole section.
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
    dddd = '0002'
    diff_subdirs('/home/yzan/Desktop/try/%s' % dddd, '/home/yzan/Desktop/arXiv/%s' % dddd)
    if parent.tag == 'outline':
        for subsec in list(parent): # If no child, list is empty
            parent.set('_note', parent.get('_note', '') + subsec.attrib['_note'] + ' \n') # don't use defaultdict!
            parent.remove(subsec)

# title, abstract, sections['introduction'] ... 
for child in root: # head, body
    if child.tag == 'body':
        for outline in child.iter():
            recur_rm(outline)
            flatten(outline)

outname = join(within_results('/final'), basename(fpath))
tree.write(outname) # Overwrite the original file