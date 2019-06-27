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
from os import remove, mkdir, walk, listdir
from paths import data_path
from shutil import copyfile, copytree
import fnmatch
from useFilter import mk_the_dirs

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

def main():
    rootdir = 'data/1701'
    errlogpt = 'results/%s/errCases_db/dblog.txt' % rootdir[-4:]
    outdir = dirname(errlogpt)
    bibPt = {r'(\\begin(\*)?{thebibliography}.*?\\end(\*)?{thebibliography})':''}
    mk_the_dirs([outdir])

    with open(errlogpt, 'a') as ovw_err_log:
        for rt, _, fls in walk(rootdir):
            TeXes = fnmatch.filter(fls, '*.tex')
            if len(TeXes) == 0 and basename(rt)[-5:].isdigit:
                print(basename(rt))
                
                # ovw_err_log.write('No TeX at %s \n' % rt)
                # copytree(rt, outdir + '/' + basename(rt))
        #     for itm in TeXes:
        #         inputpt = join(rt, itm)
        #         outputpt = 'results/' + rootdir[-4:] + '/db/' + itm + '_db.tex'
        #         try:
        #             subout(inputpt, outputpt, bibPt)
        #         except:
        #             fn = (basename(inputpt))
        #             copyfile(inputpt, outdir + '/%s_%s' % (dirname(fn), fn))
        #             for i in sys.exc_info():
        #                 ovw_err_log.write(str(i)+ ' ')
        #             ovw_err_log.write(' \n')
        # ovw_err_log.write('================================ \n')

if __name__ == "__main__":
    main()