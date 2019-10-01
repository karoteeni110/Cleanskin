# Cleanskin
A pipeline which converts diverse .TeX documents into XML format.

## Usage

### .tex --> .xml 

`python3 useLatexml.py`

Change the variables in `__main__` to specify src and dst:

`errlogpath`: the path of error log. E.g. 'results/latexml/errorlog.txt'

`rootdir`: the path of the directory where the article folders are. E.g. 'data/1701'

`outdir`: the destination directory for the output, i.e. xmls. E.g. 'results/latexml'



