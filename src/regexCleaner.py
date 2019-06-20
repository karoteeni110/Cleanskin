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
    For test (debib a single tex file in /data/DIRNAME):
        python3 regexCleaner.py debib [0001|0002|1701]
    For all the files in results/DIRNAME (DIRNAME can only be 0001/0002/1701):
        python3 regexCleaner.py postclean [0001|0002|1701]
"""
import re, os, sys
from paths import results_path, data_path, within_results
from specialcase_mover import get_artIDdir_in_data

VERBOSE = True
REPORT_EVERY = 100

def list_input(parentdir, dddd):
    """
    Return a list of (path, artID, filename) for each of the TeX file.
    """
    print(parentdir, dddd)
    if parentdir == 'data':
        ext, pdirpath = '.tex', data_path
    elif parentdir == 'results':
        ext, pdirpath = '_filtered.xml', results_path
    else:
        raise AssertionError('Argument error.')

    all_files = []
    dddd_dir = os.path.join(pdirpath, dddd) # data/1701 or results/0001

    for root, _, files in os.walk(dddd_dir):
        # $HOME/data/0001/=astro-ph0001306 
        # [] 
        # ['fig15b.epsi', 'fig4.epsi', 'fig1.epsi', 'paper.tex',  'fig8b.epsi', 'fig11.epsi']
        for fn in files:
            if ext in fn:
                path = os.path.join(root, fn)
                if parentdir == 'data':
                    artID = get_artIDdir_in_data(root).strip('=')
                elif parentdir == 'results':
                    artID = fn[1:-13] # TODO check this!!
                all_files.append((path,artID,fn))
    return all_files

def main():
    if sys.argv[2] not in ['1701', '0001', '0002'] \
    or sys.argv[1] not in ['debib', 'postclean'] \
    or len(sys.argv) != 3:
        raise TypeError('Argument error.') 

    # Patterns
    bib = {r'(\\begin(\*){thebibliography}.*?\\end(\*){thebibliography})':''}
    xmlImpurity = {r'((\\\[.*?\\\])|(&#[0-9]+;))':' '} 

    # Set sub mode & collect paths
    if sys.argv[1] == 'debib':
        all_input = list_input('data', sys.argv[2]) # /data/1701/*.tex
        output_path = within_results(sys.argv[2]) # results/1701/
        patterns = bib
        fname_end = '_debib.tex'
    elif sys.argv[1] == 'postclean':
        all_input = list_input('results', sys.argv[2]) # results/1701/*_filtered.xml
        output_path = within_results( '%s/%sxml' % (sys.argv[2], sys.argv[2]) ) # results/1701/1701xml/ 
        patterns = xmlImpurity
        fname_end = '.xml'


    

    for i, (fpath, artid, fname) in enumerate(all_input):
        # Read data & handle exceptions
        with open(fpath, mode='r', encoding='utf-8', errors='ignore') as texfile:
            try:
                data = texfile.read()
            except UnicodeDecodeError as e:
                # Write out the error message and skip the file; should be useless
                with open(os.path.join(within_results(sys.argv[2]), 'log/debibErr.txt'), 'a') as errorlog:
                    errorlog.write(fname + ' ' + e.reason + '\n')
                continue

        # Set verbose
        if VERBOSE:
            if len(all_input) == 1:
                every = 1
            else:
                every = REPORT_EVERY        
            if i % every == 0 or i == len(all_input)-1: 
                print('Stripping file %d: %s/%s' % (i+1, artid, fname))
    
        # Substituting
        for pt in patterns:
            clean_data = re.sub(pt, patterns[pt], data, flags=re.S | re.M | re.I)
        output_fname = os.path.join(output_path, '%s%s' % (artid, fname_end) ) # Name files with artid
        if os.path.exists(output_fname): # Check multiple tex articles
            os.remove(output_fname)
            with open(os.path.join(within_results(sys.argv[2]), 'log/00error.txt'), 'a') as errorlog:
                errorlog.write('Overwriting err at:' + fpath + '\n')
        else:
            with open(output_fname,'w') as out:
                out.write(clean_data)

    with open(os.path.join(within_results(sys.argv[2]), 'log/00error.txt'), 'a') as errorlog:
        errorlog.write('=======================' + '\n')

main()