from paths import tester_tex_path, results_dir
import re, os

# == Loading data ==
print(tester_tex_path)
with open(tester_tex_path, mode='r', encoding='utf-8') as tex_file:
    data = tex_file.read()

# == Paterns ==
# To be filtered/skipped:
witharg = '\\w+{\w+}{\d*}' 
newpage = '\\newpage'
citept = '\\cite{.*?}'
ref = '\\ref{.*?}'
label = '\\label{.*?}'
comments = '^%.*?$'
equationpt = '\\begin{equation}.*?\\end{equation}'
tabular = '\\begin{tabular}.*?\\end{tabular}'
items = '(\\begin{itemize}|\\end{itemize})' # Commands without item content
mathmodept = '(\${.*?}\$|\$\$.*?\$\$)'
macros = '(%s|%s|%s|%s|%s|%s|%s|%s|%s|%s)' % (witharg, newpage, citept, ref, label, \
        comments, equationpt, tabular, items, mathmodept)

# To be captured:
"""
Notes: 
To generalize the pattern, maybe peek first what is the command for introduction.

Known patterns:
1. ABSTRACT
\abstract{Emission in spectral lines can provide unique information...}
\begin{abstract} ... \end{abstract}

2. Intro / other secs
\chapter{Introduction}
\section{Introduction}

"""
abstract_pt = r'(\\begin{abstract}.*\\end{abstract})' # we need the full match
#middle_secs_pt = r'((\\section{.*?)(^\\section))' # only group 1 needed
secs_pt = r'(\\section{.*?)(\\begin{thebibliography})' # TODO: generalizable?
chap_pt = r'(\\chapter{.*?)(\\begin{thebibliography})'
patterns = [abstract_pt, secs_pt]

# == Filtering macros == #
# == Extracting == 
extracted = ''
for idx, pt in enumerate(patterns):
    for match in re.finditer(pt, data, re.S | re.M | re.I):
        grps = match.groups()
        if len(grps) >= 1:
            body = match.groups()[0]
        else:
            print('No match! Problematic pattern: %s' % pt)
            body = ''
        extracted += '\n\n' + body

# == Output ==
with open(os.path.join(results_dir, 'out.txt'),'w') as out:
    out.write(extracted) 