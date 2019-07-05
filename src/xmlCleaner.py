import xml.etree.ElementTree as ET
import sys
from paths import data_path
from os.path import join

tree = ET.parse(join(data_path, 'out.xml'))
root = tree.getroot()

print(root.tag)
print(root.attrib)
# for child in root:
#     print(child.tag, child.attrib)

print('===================')
def ignore_ns(root):
    for elem in root.iter():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]
        
ignore_ns(root)

for child in root:
    print(child.tag)
