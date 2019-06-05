from reader import *
from paths import *
import re, os

# == Loading data ==
print(tester_tex_path)
with open(tester_tex_path, mode='r', encoding='utf-8') as tex_file:
    data = tex_file.read()

# == Paterns ==
abstract_pt = r'\\begin{abstract}(.*?)\\end{abstract}'
intro_pt = r'\\section{[iI]ntroduction}(.*?)\\section{'


# == Output == 
section = re.findall(abstract_pt, data, re.S)
print(type(section))
# with open(os.path.join(results_dir, '/extracted.txt'),'w') as out:
#     out.write(section) 
