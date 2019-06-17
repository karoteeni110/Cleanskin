# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html
# cwd: results/1701/
set -e # Stop script if a simple command fails
for basename in =1701.*_debib.tex; do
    pandoc $basename -f latex -t opml \
    --filter /home/local/yzan/Desktop/Cleanskin/src/pandocFilter.py \
    --template=/home/local/yzan/Desktop/Cleanskin/data/temp.xml \
    -s -o 1701xml/${basename:0:11}_filtered.xml
done

# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file