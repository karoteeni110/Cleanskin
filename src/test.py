from paths import tester_tex_path, results_dir
import re, os, time

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
# Notes:
# >>> re.compile(citept)re.compile('\\\\cite{.*?}')
# >>> c = re.compile(citept)
# >>> a='\cite{fras94}'
# >>> re.sub(c,'SUBBED',a)
# 'SUBBED'
# >>> a='\\cite{fras94}'
# >>> re.sub(c,'SUBBED',a)
# 'SUBBED'
# >>> a='\\\cite{fras94}'
# >>> re.sub(c,'SUBBED',a)
# '\\SUBBED'

# To be filtered/skipped:
float_num = '(\d*(\.\d+)*?)'
witharg = '\\\w+{\w+}{\d*}*' # TODO
newpage = '(\\\newpage|\\vfill|\\vspace{.*?}|\\\large|\\bigskip|\\\par[box{.*?}])'
styles = '(\\\thispagestyle{\w+}|\\\\begin{center}|\\\end{center}|(\[%sex\])|(\[%scm\])|\\\w+size)' \
    % (float_num, float_num)
citept = '\\\cite{.*?}' # bad escape c?
ref = '\\ref{.*?}' # TODO
label = '\\\label{.*?}'
comments = '%.*?$' 
equationpt = '((\\\\begin{equation}.*?\\\end{equation})|(\\\\begin{eqarray}.*?\\\end{eqarray}))'
tabular = '(\\\\begin{table}.*?\\\end{table}|\\\\begin{tabular}.*?\\\end{tabular})' 
items = '(\\\\begin{itemize}|\\\end{itemize}|\\\item)' # Commands without item content
figbib = '(\\\\begin{figure}.*?\\\end{figure}|\\\\begin{thebibliography}.*?\\\end{thebibliography})'
mathmodept = '\$.*?\$'
macros = r'(%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s)' % (witharg, newpage, styles, citept,\
        ref, label, comments, equationpt, tabular, items, figbib, mathmodept)

begindoc = r'(.*^\\begin{document}$)' # all the code before \begin{doc}

# == Filtering macros == #
print('Stripping 1...')
start1 = time.time()
data = re.sub(begindoc,'', data, flags=re.S | re.M | re.I)
end1 = time.time()
print(end1 - start1)

# Check the match
# print(re.search(mathmodept, data, flags=re.S | re.M | re.I).group())
# exit(0)

print('Stripping 2...')
data = re.sub(macros,'', data, flags=re.S | re.M | re.I)

# Check the filtered results:
with open(os.path.join(results_dir, 'out.txt'),'w') as out:
    out.write(data)
exit(0)

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
patterns = [abstract_pt, chap_pt]

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