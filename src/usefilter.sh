# Usage:
# usefilter.sh 2> ../results/dddd/log/xmlerror.txt 

# pwd: /src
dddd='0002'
if cd ../results/${dddd}; then
    # set -e # Stop script if a simple command fails
    for basename in =*${dddd}*_debib.tex; do
        pandoc $basename -f latex -t opml \
        --filter /home/local/yzan/Desktop/Cleanskin/src/pandocFilter.py \
        --template=/home/local/yzan/Desktop/Cleanskin/data/temp.xml \
        -s -o ${dddd}filtered/${basename:0:-10}_filtered.xml
        if [ "$?" = "0" ]; then
            echo 'FILE:' $basename 'MESSAGE:' 1&>2
        fi
    done
fi

# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file
# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html