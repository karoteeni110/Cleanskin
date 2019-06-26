
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
# =========================

function call_debib {
    for tex in data/$dddd/*/*.tex; do
        OUT=results/$dddd/1/$(basename "$(dirname "$tex")")/$(basename "$tex")
        suppress_bib $tex $OUT
    done
}



function call_converter {
    for tex in results/$dddd/1/*/*.tex; do
        DIRNAME2=$(basename "$(dirname "$tex")")/$(basename "$tex")
        OUT=results/$dddd/2/${DIRNAME2:0:-4}.xml
    if mkdir $(dirname "$OUT"); then
        convert $tex $OUT
    else
        convert $tex $OUT
    fi
    if [ "$?" -eq "0" ]; then
        echo 'FILE:' $1 'MESSAGE:' 1&>2 # TODO: show the failed
    fi
    done
}



function postclean {
    for xml in results/$dddd/2/*/*.xml; do
        DIRNAME2=$(basename "$(dirname "$xml")")/$(basename "$xml")
        OUT=results/$dddd/3/${DIRNAME2:0:-4}.xml
        python3 src/regexCleaner.py postclean $xml $OUT 
        python3 src/xmlCleaner.py $OUT results/$dddd/fi/${DIRNAME2:0:-4}.xml

        if [ "$?" -eq "0" ]; then
            echo 'FILE:' $1 'MESSAGE:' 1&>2
        fi
    done
}

dddd='1701'
# call_debib |
# call_converter 2>>results/$dddd/2/log.txt |
postclean #2>>results/$dddd/fi/log.txt