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
from os import remove, mkdir
from paths import data_path
from shutil import copyfile

VERBOSE = True
REPORT_EVERY = 100

def get_artIDdir(infile):
    '''
    infile: input filepath.
    '''
    return basename(dirname(infile))

def main(pt_pairs, infile, outfile, logdir):
    '''
    pt_pairs: dictionary, in the form of {pattern: subbed_string}. 
    infile: input filepath. E.g. 'data/1701/*/*.tex'
    outfile: output filepath. E.g. 'results/1701/XXX/x.tex'
    logdir: directory path for errlog and problematic files.
    '''
    # Read data & handle exceptions
    ovw_err_log = open(join(dirname(dirname(outfile)),'00error.txt'), 'a')

    with open(infile, mode='r', encoding='utf-8', errors='ignore') as texfile:
        data = texfile.read()

    # Substituting
    for pt in pt_pairs:
        clean_data = re.sub(pt, pt_pairs[pt], data, flags=re.S | re.M | re.I)

    if exists(outfile): # Avoid overwriting
        ovw_err_log.write('Overwriting err:' + outfile + '\n')
    else:
        try:
            mkdir(dirname(outfile))
        except FileExistsError:
            pass
        with open(outfile,'w') as out:
            out.write(clean_data)

    ovw_err_log.close()

if __name__ == "__main__":

    bib = {r'(\\begin(\*){thebibliography}.*?\\end(\*){thebibliography})':''}
    main(bib, sys.argv[2], sys.argv[3])