"""
Cleans {thebibliography} section before using Pandoc. 

Usage: 
    For test (debib a single tex file in /data):
        python3 noBib.py TEX_FILE_NAME 
    For all the files in /data:
        python3 noBib.py GOGOGO
"""
import re, os, sys
from paths import results_dir, data_path

VERBOSE = False
REPORT_EVERY = 5

def list_input(arg):
    """
    Return a list of (path, filename) for each of the .tex.
    """
    if arg != 'GOGOGO':
        all_files = [ (os.path.join(data_path, arg), arg) ]
    else:
        all_files = []
        for root, _, folderfiles in os.walk(data_path):
            for singlefile in folderfiles:
                if '.tex' in singlefile:
                    all_files.append((os.path.join(root, singlefile), singlefile))
    return all_files

def main():
    # Read data
    all_files = list_input(sys.argv[1])

    # Pattern
    bib = r'(\\begin{thebibliography}.*?\\end{thebibliography})'
    
    # Substitute & write out
    for i, (fpath, fname) in enumerate(all_files):
        with open(fpath, mode='r', encoding='utf-8') as texfile:
            data = texfile.read()

        if VERBOSE:
            if len(all_files) == 1:
                every = 1
            else:
                every = REPORT_EVERY        
            if i % every == 0 or i == len(all_files)-1: 
                print('Stripping file %d: %s' % (i+1, fname))

        clean_data = re.sub(bib,'', data, flags=re.S | re.M | re.I)
        debib_fname = os.path.join(results_dir, '%s_debib.tex' % fname[:-4])
        print(debib_fname)
        with open(debib_fname,'w') as out:
            out.write(clean_data)
            
if __name__ == "__main__":
    main()