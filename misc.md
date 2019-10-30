## cs0303019
Sections are garbled.

##  Mallet usage

```
# Import fulltext data
./bin/mallet import-dir --input ~/Desktop/Cleanskin/results/cs_lda/fulltext --output cs_fulltext.mallet --keep-sequence --remove-stopwords

# Import abstract data
./bin/mallet import-dir --input ~/Desktop/Cleanskin/results/cs_lda/abstract --output cs_abstract.mallet --keep-sequence --remove-stopwords

# Get model and inferencer (take hours)
./bin/mallet train-topics --input cs_fulltext.mallet --num-topics N --output-model cs_ftmodel_100tpc.mallet --output-doc-topics cs_ft_composition_100tpc.txt --output-topic-keys cs_ft_keys_100tpc.txt --inferencer-filename cs_ft_inferencer_100tpc.mallet

# Infer & get distribution (fast)
./bin/mallet infer-topics --inferencer cs_ft_inferencer_100tpc.mallet --input cs_abstract.mallet --output-doc-topics cs_abt_composition_100tpc.txt
```

`XXX_keys.txt`: topic words

`cs_XX_composition_Xtpc.txt`: topic distributions

Time usage: 12~13 hours for 100 topics from 140k articles

## ML catelogs

```
>> print(Counter(ml_inlist.catecount))
Counter({0: 9642, 1: 8963, 2: 3507, 3: 697, 4: 76, 5: 2})
```

## Neural catelogs

```
>> print(Counter(neural_inlist.catecount))
Counter({0: 1063, 1: 1507, 2: 1044, 3: 278, 4: 31, 5: 2})
``` 




