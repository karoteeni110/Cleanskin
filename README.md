# Cleanskin
A pipeline which converts diverse .TeX documents into XML format.

The "pipes":

<ul>
<li>Removing bibliography with RegEx -> </li> 
<li>Convert TeXes with Pandoc & filter -> </li>
<li>Clean the unrecognized formats with RegEx -> </li>
<li>Done. </li>
</ul>

## Pipeline

1. ``python3 src/noBib.py DIRNAME``

Cleans {thebibliography} in the TeX code before using Pandoc.

2. ``python3 specialcase_mover.py 1701/log/00error.txt``

If there happens error during bibliography removing, check results/DIRNAME/log/00error.txt and remove the problematic articles into data/specialcase/DIRNAME.

3. ``usefilter.sh 2> log/xmlerror.txt``

Use Pandoc and format filter (src/pandocFilter.py) to convert results/DIRNAME/*_debib.tex into XMLs.
