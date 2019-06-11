# pandoc -s ../data/paper.tex --filter beheading.py -o output.xml
pandoc ../data/paper.tex -f latex -t opml -s -o out.xml
# pandoc -s ../data/example.text -o output.xml
