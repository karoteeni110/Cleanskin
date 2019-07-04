import xml.etree.ElementTree as ET
import sys

tree = ET.parse('../data/out.xml')
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

print(len([elem.attrib for elem in root.iter()]))
# def no_math(rt):
#     for math in rt.iter('Math'):
