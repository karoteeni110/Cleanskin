from reader import *
from paths import *
import re, os

# == Loading data ==
print(tester_tex_path)
with open(tester_tex_path, mode='r', encoding='utf-8') as tex_file:
    data = tex_file.read()

# == Paterns ==
# To be filtered/skipped:
macro = '\\\w'
citept = '\\cite{.*?}'
ref = '\\ref{.*?}'
label = '\\label{.*?}'
comments = '^%.*?$'
equationpt = '\\begin{equation}.*?\\end{equation}'
mathmodept = '(\${.*?}\$|\$\$.*?\$\$)'
macros = '(%s|%s|%s|%s|%s|%s)' % (citept, ref, label, comments, equationpt, mathmodept)

# To be captured:
abstract_pt = r'(\\begin{abstract}.*\\end{abstract})' # we need the full match
#middle_secs_pt = r'((\\section{.*?)(^\\section))' # only group 1 needed
last_sec_pt = r'(\\section{.*?)(\\begin{thebibliography})'
patterns = [abstract_pt, last_sec_pt]

# == Filtering macros == #
# == Extracting == 
extracted = ''
for idx, pt in enumerate(patterns):
    for match in re.finditer(pt, data, re.S | re.M | re.I):
        body = match.groups()[0]
        extracted += '\n\n' + body

# == Output ==
with open(os.path.join(results_dir, 'out.txt'),'w') as out:
    out.write(extracted) 