"""Load gensim topic model to infer section compositions"""

from sys import exit, argv, stderr
import os.path
import re, pickle, psutil, sys, traceback
from os import listdir
from paths import data_path
import numpy as np

from nltk.tokenize import RegexpTokenizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel,LdaMulticore

def tokenize_filter(docs) :
    # tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        docs[idx] = re.split(r'\s',docs[idx])  # Split into words.
        if (idx+1)%1000==0:
            print(idx, '/', range(len(docs)))
    return docs

# if len(argv) != 6 :
#     print("Usage: {} <model_path> <catedoc_pkl_path> <dst_dir>\n".format(argv[0]))
#     exit(1)

# ft_fname = argv[1]
# ab_fname = argv[2]
# results_dir = argv[3]
# num_topics = [ int(i) for i in argv[4].split(',')] #int(argv[4])
# random_seed = int(argv[5])

# if not os.path.exists(results_dir) :
#     print("{} does not exist, exiting...\n".format(results_dir), file=stderr)
#     exit(1)

print("Reading cates...")
with open(ab_fname, 'rb') as f:
    ab_ids,ab_docs = pickle.load(f) # extract_documents(ab_fname, whitelist)
print("read", len(ab_docs),"documents")

print("tokenizing...")
ab_docs = tokenize_filter(ab_docs)

print("loading dictionary...")
dictionary = 0 # Dictionary(docs)
print('Number of unique tokens: %d' % len(dictionary))

print('loading corpus...')
corpus = 0 #[dictionary.doc2bow(doc) for doc in docs]
ab_corpus = [dictionary.doc2bow(doc) for doc in ab_docs]


# Train LDA model.
chunksize = 2000
passes = 10      # num epoches
iterations = 50   # max passes of E-step
eval_every = None

# Make a index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

for t in num_topics :

    print("topics = {}".format(t))

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=t,
        passes=passes,
        eval_every=eval_every,
        random_state=random_seed,
        dtype=np.float64
    )

    top_topics = model.top_topics(corpus, docs, dictionary, coherence='c_v', topn=20, processes=4)

    topic_dist = model.get_document_topics(ab_corpus)
    with open(results_dir + '/%d_%d_abstract_composition_compact.txt' % (t, random_seed), 'w') as f :
        for id,d in zip(ids, topic_dist) :
            print(id, ' '.join(["%d=%f" % (tid,prob) for tid,prob in d ]), file=f)

    with open(results_dir + '/%d_%d_abstract_composition.txt' % (t, random_seed), 'w') as f :
        for id,d in zip(ids, topic_dist) :
            remainder = 0.0 if (len(d) == t) else (1.0 - sum([ prob for _,prob in d ])) / float(t - len(d))
            tmp = dict(d)
            print(id, ' '.join([str(tmp.get(i, remainder)) for i in range(t)]), file=f)

