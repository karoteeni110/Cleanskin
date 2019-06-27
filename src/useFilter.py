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

fromfile, tofile = '', ''
a = run('pandoc %s -f latex -t opml\
    --filter src/pandocFilter.py\
    --template=data/temp.xml\
    -s -o %s' % (fromfile, tofile), \
    shell=True, stdout=PIPE, stderr=PIPE)
for i in [a.stderr, a.stdout]:
    if i != b'': # stderr an stdout should BOTH be null if convertion succeeds


# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file
# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html