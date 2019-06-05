from reader import *
from paths import *
import re, os

# == Loading data ==
print(tester_tex_path)
with open(tester_tex_path, mode='r', encoding='utf-8') as tex_file:
    data = tex_file.read()

# == Paterns ==
abstract_pt = r'(\\begin{abstract}.*?\\end{abstract})'
intro_pt = r'(\\section{[iI]ntroduction}.*?\\section{)'
othersec_pt = r'((\\section{.*?)(\\section|\n\n))'
patterns = [abstract_pt, intro_pt, othersec_pt]

# == Output == 
sections = []
for pt in patterns:
    sec = re.findall(pt, data, re.S)
    if len(sec)>1:
        print(sec)
    sections.extend(sec)
exit(0)
with open(os.path.join(results_dir, 'out.txt'),'w') as out:
    print(sections)
    extracted = ' '.join(sections)
    out.write(extracted) 
