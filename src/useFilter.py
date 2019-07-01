# Usage:
# usefilter.sh 2> ../results/dddd/log/xmlerror.txt 

# pwd: /src
# dddd='1701'

# for artid in results/${dddd}/*; do
#     if 
#     echo $artid/*.tex 
#     # pandoc $artid/*.tex -f latex -t opml \
#     # --filter src/pandocFilter.py \
#     # --template=data/temp.xml \
#     # -s -o results/${dddd}/opml/$(basename "$artid").xml
#     if [ "$?" = "0" ]; then
#         echo 'FILE:' $tex 'MESSAGE:' 1&>2
#     fi
# done

from subprocess import run, PIPE
from shutil import copyfile, copytree, rmtree
from os import walk, mkdir, stat, remove
from os.path import basename, dirname, exists

def pandoc(from_fpath, to_fpath):
    a = run('pandoc %s -f latex -t opml\
        --filter src/pandocFilter.py\
        --template=data/temp.xml\
        -s -o %s 2>&1' % (from_fpath, to_fpath), shell=True, stdout=PIPE)
    return a

def check_err(cmd, inputfile, outfile, errFileDest, errlog):
    if cmd.stdout != b'': # stderr an stdout should BOTH be null if convertion succeeds
        # try:
        #     copyfile(inputfile, errFileDest + '/%s' % basename(inputfile))
        # except FileNotFoundError:
        copytree(dirname(inputfile), errFileDest + '/%s' % basename(dirname(inputfile)))
        errlog.write(inputfile + ' \n' + cmd.stdout.decode('utf-8'))
        errlog.write('========================================= \n')

        if exists(outfile):
            if stat(outfile).st_size == 0:
                remove(outfile)

def check_redo_err(cmd, inputfile, outfile, errFileDest, errlog):
    if cmd.stdout != b'': # stderr an stdout should BOTH be null if convertion succeeds
        errlog.write(inputfile + ' \n' + cmd.stdout.decode('utf-8'))
        errlog.write('========================================= \n')
    
    if exists(outfile):
        if stat(outfile).st_size == 0:
            remove(outfile)
        else:
            rmtree(dirname(inputfile))
            print('%s; Done & rm: %s ' % (cmd.stdout, dirname(inputfile)))

def mk_the_dirs(dirpaths):
    for i in dirpaths:
        try:
            mkdir(i)
        except FileExistsError:
            pass
    
def main(rootdir):
    articles = next(walk(rootdir))[1]
    errFileDir = dirname(rootdir) + '/errCases_opml'
    elp = errFileDir + '/log.txt'
    
    mk_the_dirs([errFileDir])

    with open(elp, 'a') as errlog:
        for art in articles:
            fromfile = rootdir + '/' + art + '/*.tex'
            tofile = dirname(rootdir) + '/opml/' + art + '.xml'
            cmd = pandoc(fromfile, tofile)
            check_err(cmd, fromfile, tofile, errFileDir, errlog)

def errcase_redo(rootdir):
    articles = next(walk(rootdir))[1]
    errFileDir = rootdir
    elp = errFileDir + '/REDOlog.txt'

    with open(elp, 'a') as errlog:
        for art in articles:
            if art[-1].isdigit():
                fromfile = rootdir + '/' + art + '/*.tex'
                tofile = dirname(rootdir) + '/opml/' + art + '.xml'
                cmd = pandoc(fromfile, tofile)
                check_redo_err(cmd, fromfile, tofile, errFileDir, errlog)

if __name__ == "__main__":
    # main('results/0002/db')
    errcase_redo('results/0001/errCases_db')
# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON *.tex > pandoAST.json # Check the AST of the file
# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html
# pandoc *.tex -s -f latex -t opml --filter /home/yzan/Desktop/Cleanskin/src/pandocFilter.py --template=/home/yzan/Desktop/Cleanskin/data/temp.xml -s -o out.xml
