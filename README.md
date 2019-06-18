# Cleanskin
A pipeline which converts diverse .TeX documents into XML format.

The "pipes":

- Removing bibliography (regexCleaner.py) -> 

- Convert TeXes (usefilter.sh) -> 

- Clean the unrecognized formats (regexCleaner.py) -> 

- Removing unrecognized references & acknowledgements (xmlCleaner.py) ->

- Done.


## Pipelines

> python3 regexCleaner.py debib DIRNAME 

Cleans {thebibliography} in the TeX code before using Pandoc.

> python3 specialcase_mover.py 1701/log/00error.txt 

If there happens error during bibliography removing, check results/DIRNAME/log/00error.txt and remove the problematic articles into data/specialcase/DIRNAME.

> usefilter.sh 2> log/xmlerror.txt 

Use Pandoc and format filter (src/pandocFilter.py) to convert results/DIRNAME/*_debib.tex into XMLs.

_TODO: handle exceptions_

> python3 regexCleaner.py postclean DIRNAME

Cleans the XML characters (e.g. '&\#10;', '&amp\;') and refs ('\\[sec:summery\\]') 
after it.

> python3 xmlCleaner.py 

_TODO: design the usage_

_TODO: clean data picker_