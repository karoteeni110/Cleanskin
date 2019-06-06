from reader import *
from paths import *
import re, os

# == Loading data ==
print(tester_tex_path)
with open(tester_tex_path, mode='r', encoding='utf-8') as tex_file:
    data = tex_file.read()

# == Paterns ==
abstract_pt = r'(\\begin{abstract}.*\\end{abstract})' # we need the full match
intro_pt = r'(\\section{[iI]ntroduction}.*)(\\section{)' # only group 1 needed
othersecs_pt = r'(\\section{.*)(\\section|\n\n)' # only group 1 needed
patterns = [abstract_pt, intro_pt, othersecs_pt]

# == Extracting == 
extracted = ''
for idx, pt in enumerate(patterns):
    for match in re.finditer(pt, data, re.S):
        if idx == 0:  
            grp = 0 # fetch full match for abstract section
        else:
            grp = 1 # group 1 for other sections
        body = match.group(grp) 
    extracted += '\n\n' + body

# == Output ==
with open(os.path.join(results_dir, 'out.txt'),'w') as out:
    out.write(extracted) 
