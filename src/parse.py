import xml.etree.ElementTree as ET
import pickle
from os.path import join
from newCleaner import get_root, is_section
from paths import results_path


path = '/home/yzan/Desktop/Cleanskin/results/cleaned_xml/=1701.00077.xml'
_, root = get_root(path)

def get_headings(xmlpath):
    _, root = get_root(xmlpath)
    secdict = {}
    for elem in root:
        if is_section()