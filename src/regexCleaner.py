"""
Cleans {thebibliography} section before using Pandoc 
OR 
the XML characters (e.g. '&#10;', '&amp;') and refs ('\[sec:summery\]') 
after it.

Output:
debib: writes out cleaned tex files into /result and rename them in the format
e.g. '=1701.01278_debib.tex'.
postclean: writes out into /result/DIRNAME and rename them in the format
e.g. '=1701.01278.xml'

Assumes all the latex file end with ".tex".

Usage:
    python3 regexCleaner.py $INPUT_FILENAME $OUTPUT_FILENAME
    python3 regexCleaner.py $INPUT_FILENAME $OUTPUT_FILENAME
"""
import re, sys
from os.path import relpath, exists, join, dirname, basename
from os import remove, mkdir, walk
from paths import data_path
from shutil import copyfile
import fnmatch

def get_artIDdirs_in_data(dddd):
    artIDs = next(walk(join(data_path, dddd)))
    return artIDs[1]

def subout(inpath, outpath, pt_pairs):
    with open(inpath, mode='r', encoding='utf-8', errors='ignore') as texfile:
        data = texfile.read()

    # Substituting
    for pt in pt_pairs:
        clean_data = re.sub(pt, pt_pairs[pt], data, flags=re.S | re.M | re.I)
        try:
            mkdir(dirname(outpath))
        except FileExistsError:
            pass
        with open(outpath,'w') as out:
            out.write(clean_data)

def iter_dirs(anotherFunc, extraArgs, rootdir, fnpattern, out_suffix, capture_err_type, errlog_path):
    errlog = open(errlog_path, 'a')
    for rt, _, fls in walk(rootdir):
        for itm in fnmatch.filter(fls, fnpattern):
            inpath = join(rt, itm)
            outpath = 'results' +inpath.strip('data').strip('.tex') + out_suffix
            try:
                anotherFunc(inpath, outpath, *extraArgs)
            except capture_err_type:
                copyfile(inpath, errlog_path)
                errlog.write()



def main(inputdir, subPtDict, errlogpath):
    """
    subPtDict: dictionary, in the form of {pattern: subbed_string}. 
    inputdir: 'data/1701'
    logdir: directory path for errlog and problematic files.
    """
    # Read data & handle exceptions
    ovw_err_log = open(errlogpath, 'a')
    for rt, _, fls in walk(inputdir):
        for itm in fnmatch.filter(fls, '*.tex'):
            inputpt = join(rt, itm)
            outputpt = 'results' + inputpt.strip('data').strip('.tex') + '_db.tex'
            try:
                subout(inputpt, subPtDict)
            except:
                copyfile(inputpt, dirname(errlogpath))
                for i in sys.exc_info():
                    ovw_err_log.write(str(i)+ ' ')
                ovw_err_log.write(' \n')
    ovw_err_log.write('================================ \n')
    ovw_err_log.close()

if __name__ == "__main__":
    # VERBOSE, REPORT_EVERY = True, 100
    dddd = 'data/1701'
    errlogpath = 'results/%s/log/debibErr.txt' % dddd[-4:]
    bibPt = {r'(\\begin(\*)?{thebibliography}.*?\\end(\*)?{thebibliography})':''}
    try:
        mkdir(dirname(errlogpath))
    except FileExistsError:
        pass
    main(dddd, bibPt, errlogpath)


    """
    >>> for rt, dirn, fls in walk('1701short'):
    ...     print(rt)
    ...     print(dirn, fls)
    ...     print()
    ... 
    1701short
    ['1701.01247', '1701.01020', '1701.01292'] []

    1701short/1701.01247
    [] ['withdrawn']

    1701short/1701.01020
    [] ['withdrawn']

    1701short/1701.01292
    ['test'] ['withdrawn']

    1701short/1701.01292/test
    [] ['try']

    """