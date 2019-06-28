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
from shutil import copyfile, copytree
from os import walk, mkdir, stat, remove
from os.path import basename, dirname, exists

def pandoc(from_fpath, to_fpath):
    a = run('pandoc %s -f latex -t opml\
        --filter src/pandocFilter.py\
        --template=data/temp.xml\
        -s -o %s' % (from_fpath, to_fpath), shell=True, stdout=PIPE, stderr=PIPE)
    return a

def check_err(cmd, inputfile, outfile, errFileDest, errlog):
    for stdmsg in [cmd.stderr, cmd.stdout]:
        if stdmsg != b'': # stderr an stdout should BOTH be null if convertion succeeds
            # try:
            #     copyfile(inputfile, errFileDest + '/%s' % basename(inputfile))
            # except FileNotFoundError:
            copytree(dirname(inputfile), errFileDest + '/%s' % basename(dirname(inputfile)))
            errlog.write(inputfile + ' \n' + stdmsg.decode('utf-8'))
            errlog.write('========================================= \n')

            if exists(outfile):
                if stat(outfile).st_size == 0:
                    remove(outfile)
                # errlog.write(inputfile + ' Invisible failure : Output empty.')
                # errlog.write('========================================= \n')

def mk_the_dirs(dirpaths):
    for i in dirpaths:
        try:
            mkdir(i)
        except FileExistsError:
            pass
    
def main():
    rootdir = 'results/1701/db'
    articles = next(walk(rootdir))[1]
    errFileDir = rootdir.strip('db') + 'errCases_opml'
    elp = errFileDir + '/log.txt'
    
    mk_the_dirs([errFileDir])

    with open(elp, 'a') as errlog:
        for art in articles:
            fromfile = rootdir + '/' + art + '/*.tex'
            tofile = rootdir.strip('db') + 'opml/' + art + '.xml'
            cmd = pandoc(fromfile, tofile)
            check_err(cmd, fromfile, tofile, errFileDir, errlog)
            
if __name__ == "__main__":
    main()
# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.json # Check the AST of the file
# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html