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

VERBOSE = True
REPORT_EVERY = 5
def list_input(arg):
    if arg != 'GOGOGO':
        all_files = [ os.path.join(data_path, arg) ]
    else:
        all_files = []
        for root, _, folderfiles in os.walk(data_path):
            for singlefile in folderfiles:
                if '.tex' in singlefile:
                    all_files.append(os.path.join(root, singlefile))
    return all_files

def main():
    # Read data
    f = sys.argv[1]
    all_files = list_input(f)

    # Pattern
    bib = r'(\\begin{thebibliography}.*?\\end{thebibliography})'
    
    # Substitute & write out
    for fpath in all_files:
        with open(fpath, mode='r', encoding='utf-8') as texfile:
            data = texfile.read()

        if VERBOSE:
            if len(all_files)==1:
                REPORT_EVERY = 1
            for i in range(1,len(all_files), REPORT_EVERY):
                print('Stripping file %d: %s' % (i, f))

        clean_data = re.sub(bib,'', data, flags=re.S | re.M | re.I)

        with open(os.path.join(results_dir, '%s_debib.tex' % f[:-4]),'w') as out:
            out.write(clean_data)
            
if __name__ == "__main__":
    main()