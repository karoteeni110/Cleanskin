# Usage:
# usefilter.sh 2> ../results/dddd/log/xmlerror.txt 

# pwd: /src
dddd='/0002'

for tex in data${dddd}/*; do
    pandoc $tex/*.tex -f latex -t opml \
    --filter /src/pandocFilter.py \
    --template=/data/temp.xml \
    -s -o results${dddd}/$(basename "$tex").xml
    if [ "$?" = "0" ]; then
        echo 'FILE:' $basename 'MESSAGE:' 1&>2
    fi
done


# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file
# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html