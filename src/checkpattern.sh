#!/bin/bash
# grep '[Ii]ntroduction' ./*/*.tex > intro.txt
# grep 'thebibliography' ./*/*.tex > bib.txt
grep 'begin{document}' ./*/*.tex > starter.txt
wc -l starter.txt