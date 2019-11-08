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

# 
./bin/mallet evaluate-topics 

# Infer topics with loop
for i in `seq 50 50 1000`; do echo $i; ./bin/mallet infer-topics --inferencer ../csmodels/model_${i}/cs_ft_inferencer.mallet --input cs_10test.mallet --output-doc-topics cs_testcomp/cs_test_composition_${i}tpc.txt; done

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

## CS, math, physics article numbers
```
$ grep "</article>" Physics.xml | wc -l
1022424

$ grep "</article>" Computer_Science.xml | wc -l
224425 (131703)

$ grep "</article>" Mathematics.xml | wc -l
419265
```

## Split math papers

Summary:
DG : 7062
CT : 667
NT : 6538
CA : 3584
SG : 1137
QA : 2712
MP : 7978
KT : 666
IT : 7533
CO : 10008
GN : 762
NA : 4549
AP : 9737
RA : 2542
AT : 1795
LO : 2115
CV : 2606
DS : 5175
SP : 1131
AC : 2094
HO : 478
GR : 3305
OC : 5222
AG : 8136
RT : 3187
FA : 4658
GT : 3437
ST : 2636
ph : 7994
OA : 1847
GM : 552
MG : 1423
PR : 8430

## seq echo
```
y@whq-58:~$ for i in `seq 50 50 1000`; do echo $i; done
50
100
150
200
250
300
350
400
450
500
550
600
650
700
750
800
850
900
950
1000
```