"""Load gensim topic model to infer section compositions"""

from sys import exit, argv, stderr
import os.path
import re, pickle, psutil, sys, traceback
from os import listdir
#from paths import data_path
import numpy as np

from nltk.tokenize import RegexpTokenizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel,LdaMulticore

def tokenize_filter(docs) :
    # tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        docs[idx] = re.split(r'\s',docs[idx])  # Split into words.
        if (idx+1)%1000==0:
            print(idx, '/', len(docs))
    return docs

if len(argv) != 6 :
    print("Usage: {} <fulltext_pkl> <catetext_pkl> <dst_dir> <model_path> <catename>\n".format(argv[0]))
    exit(1)

ft_fname = argv[1]
ab_fname = argv[2]
results_dir = argv[3]
model_path = argv[4]
catename = argv[5]

if not os.path.exists(results_dir) :
    print("{} does not exist, exiting...\n".format(results_dir), file=stderr)
    exit(1)

print("Reading fulltext...")
with open(ft_fname, 'rb') as f:
    ids,docs = pickle.load(f)
print("read", len(docs),"documents")

print("Reading cates...")
with open(ab_fname, 'rb') as f:
    ab_ids,ab_docs = pickle.load(f) # extract_documents(ab_fname, whitelist)
print("read", len(ab_docs),"documents")

print("tokenizing...")
docs = tokenize_filter(docs)
ab_docs = tokenize_filter(ab_docs)

print("loading dictionary...")
dictionary = Dictionary(docs)
dictionary.filter_extremes()
print('Number of unique tokens: %d' % len(dictionary))

print('loading corpus...')
corpus = [dictionary.doc2bow(doc) for doc in docs]
ab_corpus = [dictionary.doc2bow(doc) for doc in ab_docs]


# Load LDA model.

# Make a index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

model_fn = os.path.basename(model_path)
t,random_seed = model_fn.split('_')[:2]
print("model = {}".format(model_fn))
model = LdaModel.load(model_path, mmap='r')

topic_dist = model.get_document_topics(ab_corpus)
with open(results_dir + '/%d_%d_%s_composition_compact.txt' % (t, random_seed, catename), 'w') as f :
    for id,d in zip(ids, topic_dist) :
        print(id, ' '.join(["%d=%f" % (tid,prob) for tid,prob in d ]), file=f)

with open(results_dir + '/%d_%d_%s_composition.txt' % (t, random_seed, catename), 'w') as f :
    for id,d in zip(ids, topic_dist) :
        remainder = 0.0 if (len(d) == t) else (1.0 - sum([ prob for _,prob in d ])) / float(t - len(d))
        tmp = dict(d)
        print(id, ' '.join([str(tmp.get(i, remainder)) for i in range(t)]), file=f)

