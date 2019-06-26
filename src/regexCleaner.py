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

def get_artIDdirs_in_data(dddd):
    artIDs = next(walk(join(data_path, dddd)))
    return artIDs[1]

def searsub(infile, pt_pairs, outfile, errlog):
    with open(infile, mode='r', encoding='utf-8', errors='ignore') as texfile:
        data = texfile.read()

    # Substituting
    for pt in pt_pairs:
        clean_data = re.sub(pt, pt_pairs[pt], data, flags=re.S | re.M | re.I)

    if exists(outfile): # Avoid overwriting; should be trivial
        errlog.write('Overwriting err:' + outfile + '\n')
        
    else:
        try:
            mkdir(dirname(outfile))
        except FileExistsError:
            pass
        with open(outfile,'w') as out:
            out.write(clean_data)

def main(pt_pairs, inpt, outpt, logdir):
    '''
    pt_pairs: dictionary, in the form of {pattern: subbed_string}. 
    inpt: input file's path. E.g. 'data/1701/*/*.tex'
    outpt: output file's path. E.g. 'results/1701/XXX/x.tex'
    logdir: directory path for errlog and problematic files.
    '''
    # Read data & handle exceptions
    ovw_err_log = open(join(dirname(dirname(inpt)),'debib_error.txt'), 'a')
    searsub(inpt, pt_pairs, outpt, ovw_err_log)
    ovw_err_log.close()



if __name__ == "__main__":
    VERBOSE = True
    REPORT_EVERY = 100
    bib = {r'(\\begin(\*)?{thebibliography}.*?\\end(\*)?{thebibliography})':''}
    main(bib, '/home/yzan/Desktop/try/cluster/=astro-ph0001113/paper.tex', '/home/yzan/Desktop/try/cluster/paper_debib.tex', '/home/yzan/Desktop/try/cluster')