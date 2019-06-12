"""
Cleans \bib{thebibliography} section before using Pandoc. 
"""
import re, os

# Read data
tester_tex_path = '/home/local/yzan/Desktop/Cleanskin/data/nat_orders_revisionv4Amaro.tex'
with open(tester_tex_path, mode='r', encoding='utf-8') as tex_file:
    data = tex_file.read()

# Patterns
bib = r'(\\begin{figure}.*?\\end{figure}|\\begin{thebibliography}.*?\\end{thebibliography})'

# Substitute & write out
print('Stripping macros...')
clean_data = re.sub(bib,'', data, flags=re.S | re.M | re.I)

results_dir = '/home/local/yzan/Desktop/Cleanskin/results'
with open(os.path.join(results_dir, 'out.tex'),'w') as out:
    out.write(clean_data)