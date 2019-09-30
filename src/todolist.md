## cs0303019
Sections are garbled.

##  Mallet usage

```
./bin/mallet import-dir --input ~/Desktop/Cleanskin/results/cs_lda/fulltext --output cs_fulltext.mallet --keep-sequence --remove-stopwords

./bin/mallet import-dir --input ~/Desktop/Cleanskin/results/cs_lda/abstract --output cs_abstract.mallet --keep-sequence --remove-stopwords

./bin/mallet train-topics --input cs_fulltext.mallet --num-topics 100 --output-model cs_ftmodel.mallet --output-doc-topics cs_ft_composition.txt --output-topic-keys cs_ft_keys.txt --inferencer-filename cs_ft_inferencer.mallet

./bin/mallet infer-topics --inferencer cs_ft_inferencer.mallet --input cs_abstract.mallet --output-doc-topics cs_abt_composition.txt
```

(Keyword .txt files (`XXX_keys.txt`) are just for checking if model is working well.)

Distributions: cs_XX_composition.txt

Time usage for the model: 12~13 hours for corpus with 140,000+ articles