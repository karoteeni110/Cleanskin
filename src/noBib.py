"""
Cleans {thebibliography} section before using Pandoc. 
"""
import re, os, sys
from paths import results_dir, data_path

# Read data
f = sys.argv[1]
fpath = os.path.join(data_path, f)
with open(fpath, mode='r', encoding='utf-8') as texfile:
    data = texfile.read()

# Patterns
bib = r'(\\begin{thebibliography}.*?\\end{thebibliography})'

# Substitute & write out
print('Stripping bibliography...')
clean_data = re.sub(bib,'', data, flags=re.S | re.M | re.I)

with open(os.path.join(results_dir, '%s_debib.tex' % f[:-4]),'w') as out:
    out.write(clean_data)