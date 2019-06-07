from paths import tester_tex_path, results_dir
import re, os

def check_match(subbed, original):
    if subbed == original:
        print('No match!')
    else:
        print('MATCHED! ')

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
comments = r'^%.*?$'
equationpt = '\\begin{equation}.*?\\end{equation}'
tabular = '\\begin{tabular}.*?\\end{tabular}'
items = '(\\begin{itemize}|\\end{itemize})' # Commands without item content
mathmodept = '(\${.*?}\$|\$\$.*?\$\$)'
newcommand = '\\newcommand.*?$'
macros = '(%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s)' % (witharg, newpage, citept, ref, label, \
        comments, equationpt, tabular, items, mathmodept, newcommand)

begindoc = r'(.*^\\begin{document}$)' # all the code before \begin{doc}
# == Filtering macros == #
d2 = re.sub(begindoc,'', data, flags=re.S | re.M | re.I)
print(d2[:4000])
print('==!!==')
d3 = re.sub(comments,'', d2, flags=re.S | re.M | re.I)
print(d3[:4000])
exit(0)
#re.sub(comments,'', d3, flags=re.S | re.M | re.I)
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