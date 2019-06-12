# pandoc ../data/paper.tex -f latex -t opml -s -o non-filtered.xml
# pandoc ../data/paper.tex -f latex -t opml --filter pandocFilter.py -s -o filtered.xml
pandoc -s ../data/paper.tex -o paper.html
# pandoc -s -t native ../data/paper.tex > pandoAST.txt # Check the AST of the file
