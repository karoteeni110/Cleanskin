"""
Cleans {thebibliography} section before using Pandoc. 

Writes out cleaned tex files into /result, renaming it 
with "subdirname_debib.tex".

Assumes all the latex file ending with ".tex".

Usage: 
    For test (debib a single tex file in /data):
        python3 noBib.py TEX_FILE_NAME 
    For all the files in DIRNAME in /data (DIRNAME can only be 0001/0002/1701):
        python3 noBib.py DIRNAME
"""
import re, os, sys
from paths import results_dir, data_path, debib_dir

VERBOSE = True
REPORT_EVERY = 100
DIRNAMES_IN_DATA = ['0001', '0002', '1701']

def list_input(arg):
    """
    Return a list of (path, subdirname, filename) for each of the .tex.
    """
    if arg not in DIRNAMES_IN_DATA:
        all_files = [ (os.path.join(data_path, arg), arg) ]
    else:
        all_files = []
        for root, _, files in os.walk(os.path.join(data_path, arg)):
            for fn in files:
                if '.tex' in fn:
                    path = os.path.join(root, fn)
                    subdirname = os.path.basename(os.path.dirname(path))
                    all_files.append((path,subdirname,fn))
    return all_files

def main():
    # Read data
    all_tex = list_input(sys.argv[1])
    output_path = debib_dir(sys.argv[1])

    # Pattern
    bib = r'(\\begin{thebibliography}.*?\\end{thebibliography})'
    
    # Substitute & write out
    for i, (fpath, dirname, fname) in enumerate(all_tex):
        with open(fpath, mode='r', encoding='utf-8', errors='ignore') as texfile:
            try:
                data = texfile.read()
            except UnicodeDecodeError as e:
                # Write out the error message and skip the file
                with open(os.path.join(output_path, '00error.txt'), 'a') as errorlog:
                    errorlog.write(fname + ' ' + e.reason + '\n')
                continue

        if VERBOSE:
            if len(all_tex) == 1:
                every = 1
            else:
                every = REPORT_EVERY        
            if i % every == 0 or i == len(all_tex)-1: 
                print('Stripping file %d: %s/%s' % (i+1, dirname, fname))

        clean_data = re.sub(bib,'', data, flags=re.S | re.M | re.I)
        debib_fname = os.path.join(output_path, '%s_debib.tex' % dirname) # Name files with dirname
        if os.path.exists(debib_fname): # Avoid overwriting
            with open(os.path.join(output_path, 'problematic/00error.txt'), 'a') as errorlog:
                errorlog.write('MULTIPLE TEX IN ' + dirname + '\n')
            # debib_fname = os.path.join(output_path, '%s_%s_debib.tex' % (dirname, fname[:-4]))
        with open(debib_fname,'w') as out:
            out.write(clean_data)
        
if __name__ == "__main__":
    main()