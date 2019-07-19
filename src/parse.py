import xml.etree.ElementTree as ET
import pickle
from os.path import join
from xmlCleaner import get_root
from paths import results_path


path = '/home/yzan/Desktop/Cleanskin/results/cleaned_xml/=1701.00077.xml'
_, root = get_root(path)

# print(len(root))
secdict = dict()
for sec in root:
    if sec.get('title', None): # is a <section>
        secdict[sec.attrib['title']] = ''.join(sec.itertext())
    else: # is not a <section>
        secdict[sec.tag] = ''.join(sec.itertext())

for i in secdict:
    print(i, secdict[i])
    print()
# with open(join(results_path, 'test.pkl'), 'wb') as f:
    # pickle.dump(secdict, f)
