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
    python3 regexCleaner.py debib $INPUT_FILENAME $OUTPUT_FILENAME
    python3 regexCleaner.py postclean $INPUT_FILENAME $OUTPUT_FILENAME
"""
import re, sys
from os.path import relpath, exists, join, dirname
from os import remove, mkdir
from paths import data_path

VERBOSE = True
REPORT_EVERY = 100

def get_artIDdir_in_data(path, d4):
    relp = relpath(path, data_path + '/%s' % d4) # '=hep-ph0001171/mu2.tex'
    artIDdir = relp.split('/')[0] # ['=hep-ph0001171/', 'mu2.tex']
    return artIDdir

def main(mode, infile, outfile):
    bib = {r'(\\begin(\*){thebibliography}.*?\\end(\*){thebibliography})':''}
    xmlImpurity = {r'((\\\[.*?\\\])|(&#[0-9]+;))':' '} 

    # Set sub mode & collect paths
    if mode == 'debib':
        patterns = bib
    elif mode == 'postclean':
        patterns = xmlImpurity

    # Read data & handle exceptions
    ovw_err_log = open(join(dirname(dirname(outfile)),'00error.txt'), 'a')
    try:
        with open(infile, mode='r', encoding='utf-8') as texfile:
            data = texfile.read()
    except UnicodeDecodeError as e:
        ovw_err_log.write('Reading data err:' + outfile + '\n')
        ovw_err_log.write(e.reason + '\n')
        exit(0)
    
    # Substituting
    for pt in patterns:
        clean_data = re.sub(pt, patterns[pt], data, flags=re.S | re.M | re.I)

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
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    # print(sys.argv)