# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html -s -o non-filtered.html
# pandoc ../data/nat_orders_revisionv4Amaro.tex -f latex -t html --filter pandocFilter.py -s -o filtered.html
# pandoc -s ../data/nat_orders_revisionv4Amaro.tex -o paper.html
pandoc -s -t native ../data/nat_orders_revisionv4Amaro.tex > pandoAST.txt # Check the AST of the file
