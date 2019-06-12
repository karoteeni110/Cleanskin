# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html
pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t opml --filter pandocFilter.py \
--template=/home/local/yzan/Desktop/Cleanskin/data/temp.xml -s -o filtered.xml
# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
# pandoc -s -t JSON ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file