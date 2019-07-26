import xml.etree.ElementTree as ET
import pickle
from os.path import join
from xmlCleaner import get_root
from paths import results_path


path = '/home/yzan/Desktop/Cleanskin/results/cleaned_xml/=1701.00077.xml'
_, root = get_root(path)

def sec_headfreq()