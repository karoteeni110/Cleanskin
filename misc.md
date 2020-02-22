## CS
cs.LG 15590
cs.NE 2232
cs.NA 1634
cs.PF 568
cs.PL 1138
cs.CC 3171
cs.RO 2775
cs.CL 6268
cs.GR 565
cs.GT 2617
cs.NI 5056
cs.CE 1211
cs.IT 19040
cs.CG 2211
cs.IR 1718
cs.AI 6002
cs.AR 337
cs.CY 1448
cs.CV 15640
cs.GL 55
cs.CR 4252
cs.OH 482
cs.MA 853
cs.SY 4519
cs.MM 617
cs.MS 478
cs.LO 3532
cs.SD 1081
cs.SE 1779
cs.OS 140
cs.SC 894
cs.DM 4619
cs.DL 730
cs.DC 3527
cs.DB 1216
cs.ET 667
cs.DS 5981
cs.FL 1260
cs.HC 1110
cs.SI 5263
[55, 140, 337, 478, 482, 565, 568, 617, 667, 730, 853, 894, 1081, 1110, 1138, 1211, 1216, 1260, 1448, 1634, 1718, 1779, 2211, 2232, 2617, 2775, 3171, 3527, 3532, 4252, 4519, 4619, 5056, 5263, 5981, 6002, 6268, 15590, 15640, 19040]
93763 1
29961 2
7272 3
1150 4
123 5
6 6
1 7

## 6k subsample: whitelist_3000.txt

Distributed, Parallel, and Cluster Computing       3000
Networking and Internet Architecture               3000
Logic in Computer Science                          3000
Discrete Mathematics                               2998
Data Structures and Algorithms                     2997
Machine Learning                                   2992
Cryptography and Security                          2991
Computation and Language                           2989
Systems and Control                                2983
Information Theory                                 2977
Computer Vision and Pattern Recognition            2963
Social and Information Networks                    2953
Computational Complexity                           2950
Artificial Intelligence                            2914
Computer Science and Game Theory                   2720
Robotics                                           2664
Computational Geometry                             2300
Software Engineering                               2062
Neural and Evolutionary Computation                1848
Numerical Analysis                                 1718
Information Retrieval                              1687
Computers and Society                              1639
Programming Languages                              1420
Formal Languages and Automata Theory               1407
Computational Engineering, Finance, and Science    1380
Databases                                          1327
Human-Computer Interaction                         1297
Multiagent Systems                                 1023
Symbolic Computation                                979
Sound                                               968
Digital Libraries                                   850
Performance                                         718
Emerging Technologies                               705
Mathematical Software                               673
Multimedia                                          606
Graphics                                            581
Other                                               491
Hardware Architecture                               389
Operating Systems                                   175
General Literature                                   72

## cs
background 35483
related_work 31354
abstract 131703
conclusion 95520
discussion 22220
methods 55391
introduction 120070
results 69458
fulltext 131703
Summary: paper extracted: 132290 of 145428

##  Mallet usage

```
# Import fulltext data
./bin/mallet import-dir --input ~/Desktop/Cleanskin/results/cs_lda/fulltext --output cs_fulltext.mallet --keep-sequence --remove-stopwords

# Import abstract data
./bin/mallet import-dir --input ~/Desktop/Cleanskin/results/cs_lda/abstract --output cs_abstract.mallet --keep-sequence --remove-stopwords

# Get model and inferencer (take hours)
./bin/mallet train-topics --input cs_fulltext.mallet --num-topics N --output-model cs_ftmd_100tpc.mallet --output-doc-topics cs_ft_comp_100tpc.txt --output-topic-keys cs_ft_keys_100tpc.txt --inferencer-filename cs_ft_inferer_100tpc.mallet --evaluator-filename cs_ft_evaler_100tpc.mallet

# Infer & get distribution (fast)
./bin/mallet infer-topics --inferencer cs_ft_inferencer_100tpc.mallet --input cs_abstract.mallet --output-doc-topics cs_abt_composition_100tpc.txt

# Evaluate topics with loop
for i in `seq 50 50 1000`; do echo $i...; ./bin/mallet evaluate-topics --evaluator ../csmodels/model_${i}/evaluator.mallet --input cs_10test.mallet --output-doc-probs ../cs_testcomp/cs_${i}_perdoc.txt --output-prob ../cs_testcomp/cs_heldout_${i}tpc.txt; echo $i 'done'; done

# Increment

for d in ../cs_t100/*; do let "i+=1"; echo $i $d; done

for d in ../cs_t100/*; do let "i+=1"; echo $i $d; ./bin/mallet evaluate-topics --evaluator ../cs_t100/${d}/evaluator.mallet --input cs_10test.mallet --output-prob ../cs_testcomp/${d}_heldoutprob.txt; echo "...done"; done

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

### labels
```
sum([1 for i in final if 'related_work' in final[i]])
44
sum([1 for i in final if 'introduction' in final[i]])
31
sum([1 for i in final if 'methods' in final[i]])
410
sum([1 for i in final if 'back_matter' in final[i]])
57
sum([1 for i in final if 'discussion' in final[i]])
62
sum([1 for i in final if 'conclusion' in final[i]])
115
sum([1 for i in final if 'abstract' in final[i]])
1
sum([1 for i in final if 'background' in final[i]])
142
sum([1 for i in final if 'results' in final[i]])
244
```

### history
