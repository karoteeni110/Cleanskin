
#!/bin/bash

# Usage
# ./conv.sh INPUT_DIR OUTPUT_DIR

suppress_bib () {
    python3 src/regexCleaner.py debib $1 $2 # Suppress bibliography
}

convert () {
    pandoc $1 -f latex -t opml \
    --filter src/pandocFilter.py \
    --template=data/temp.xml \
    -s -o $2

}

cleanXMLChar () {
    python3 src/regexCleaner.py postclean $1 $2
}

noRefs () {
    python3 xmlCleaner.py $1 $2
}

# =========================

dddd='1701'

function call_debib {
    for tex in data/$dddd/*/*.tex; do
        OUT=results/$dddd/supbib/$(basename "$(dirname "$tex")")/$(basename "$tex")
        suppress_bib $tex $OUT
    done
}

# call_debib

function call_converter {
    for tex in results/$dddd/supbib/*/*.tex; do
        DIRNAME2=$(basename "$(dirname "$tex")")/$(basename "$tex")
        OUT=results/$dddd/xml1/${DIRNAME2:0:-4}.xml
    if mkdir $(dirname "$OUT"); then
        convert $tex $OUT
    else
        convert $tex $OUT
    fi
    if [ "$?" -eq "0" ]; then
        echo 'FILE:' $1 'MESSAGE:' 1&>2
    fi
    done
}

# call_converter 2>>results/$dddd/xml1/log.txt

function postclean {
    for xml in results/$dddd/xml1/*/*.xml; do
        DIRNAME2=$(basename "$(dirname "$xml")")/$(basename "$xml")
        OUT=results/$dddd/3/${DIRNAME2:0:-4}.xml

        #python3 src/regexCleaner.py postclean $xml $OUT 
        python3 src/xmlCleaner.py $OUT results/$dddd/fi/${DIRNAME2:0:-4}.xml

        if [ "$?" -eq "0" ]; then
            echo 'FILE:' $1 'MESSAGE:' 1&>2
        fi
    done
}

postclean #2>>results/$dddd/fi/log.txt