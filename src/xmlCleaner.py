import xml.etree.ElementTree as ET
import sys
from paths import data_path
from os.path import join
# hep-ph0001047.xml
tree = ET.parse(join(data_path, 'out.xml'))
root = tree.getroot()

def ignore_ns(root):
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]

def clean_rank1(root):
    """
    XXX: Don't do "change while iterating"!
    """

    i=0
    for child in root:
        i+=1
        print(list(root))
        if child.tag in ['resource', 'pagination']:
            print('Removed %s' % i, child)
            root.remove(child)
            print(list(root))
            print()
        else: 
            print(i, child)
            print(list(root))
            print()

ignore_ns(root)
for i, child in enumerate(root):
    print(i+1, child)
print('===========================')

clean_rank1(root)

print('===========================')
# for i, child in enumerate(root):
#     print(i+1, child)

