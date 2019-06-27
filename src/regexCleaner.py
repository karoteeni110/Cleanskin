"""
Cleans {thebibliography} section before using Pandoc 
OR 
the XML characters (e.g. '&#10;', '&amp;') and refs ('\[sec:summery\]') 
after it.
Output:
debib: writes out cleaned tex files into /result and rename them in the format
e.g. '=1701.01278_debib.tex'.
postclean: writes out into /result/DIRNAME and rename them in the format
e.g. '=1701.01278.xml'
Assumes all the latex file end with ".tex".
Usage:
    python3 regexCleaner.py $INPUT_FILENAME $OUTPUT_FILENAME
    python3 regexCleaner.py $INPUT_FILENAME $OUTPUT_FILENAME
"""
import re, sys
from os.path import relpath, exists, join, dirname, basename
from os import remove, mkdir, walk
from paths import data_path
from shutil import copyfile
import fnmatch

def subout(inpath, outpath, pt_pairs):
    with open(inpath, mode='r', encoding='utf-8', errors='ignore') as texfile:
        data = texfile.read()

    # Substituting
    for pt in pt_pairs:
        clean_data = re.sub(pt, pt_pairs[pt], data, flags=re.S | re.M | re.I)
        try:
            mkdir(dirname(outpath))
        except FileExistsError:
            pass
        with open(outpath,'w') as out:
            out.write(clean_data)
