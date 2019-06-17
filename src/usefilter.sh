# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html
# cwd: /src/
if cd ../results/0001; then
    # set -e # Stop script if a simple command fails
    for basename in =*0001*_debib.tex; do
        pandoc $basename -f latex -t opml \
        --filter /home/local/yzan/Desktop/Cleanskin/src/pandocFilter.py \
        --template=/home/local/yzan/Desktop/Cleanskin/data/temp.xml \
        -s -o 0001filtered/${basename:0:-10}_filtered.xml
    done
fi

# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file