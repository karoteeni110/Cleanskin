"""
Cleans {thebibliography} section before using Pandoc. 

Writes out cleaned tex files into /result, renaming it 
with "subdirname_debib.tex".

Assumes all the latex file ending with ".tex".

Usage: 
    For test (debib a single tex file in /data):
        python3 noBib.py TEX_FILE_NAME 
    For all the files in /data:
        python3 noBib.py GOGOGO
"""
import re, os, sys
from paths import results_dir, data_path

VERBOSE = True
REPORT_EVERY = 1

def list_input(arg):
    """
    Return a list of (path, subdirname, filename) for each of the .tex.
    """
    if arg != 'GOGOGO':
        all_files = [ (os.path.join(data_path, arg), arg) ]
    else:
        all_files = []
        for root, _, files in os.walk(data_path):
            for fn in files:
                if '.tex' in fn:
                    path = os.path.join(root, fn)
                    subdirname = os.path.basename(os.path.dirname(path))
                    all_files.append((path,subdirname,fn))
    return all_files

def main():
    # Read data
    all_files = list_input(sys.argv[1])

    # Pattern
    bib = r'(\\begin{thebibliography}.*?\\end{thebibliography})'
    
    # Substitute & write out
    for i, (fpath, dirname, fname) in enumerate(all_files):
        with open(fpath, mode='r', encoding='utf-8') as texfile:
            data = texfile.read()

        if VERBOSE:
            if len(all_files) == 1:
                every = 1
            else:
                every = REPORT_EVERY        
            if i % every == 0 or i == len(all_files)-1: 
                print('Stripping file %d: %s/%s' % (i+1, dirname, fname))

        clean_data = re.sub(bib,'', data, flags=re.S | re.M | re.I)
        debib_fname = os.path.join(results_dir, '%s_debib.tex' % dirname) # Name files with dirname
        if os.path.exists(debib_fname): # Avoid overwriting
            debib_fname = os.path.join(results_dir, '%s_%s_debib.tex' % (dirname, fname[:-4]))
        with open(debib_fname,'w') as out:
            out.write(clean_data)
        
if __name__ == "__main__":
    main()