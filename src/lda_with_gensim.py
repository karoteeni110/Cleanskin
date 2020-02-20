#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from sys import exit, argv, stderr
import os.path
import re, pickle, psutil, sys, traceback
from os import listdir
from paths import data_path
import numpy as np

from nltk.tokenize import RegexpTokenizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel,LdaMulticore

# PROCESS = psutil.Process(os.getpid())
# MEGA = 10 ** 6
# MEGA_STR = ' ' * MEGA

# def print_memory_usage():
#     """Prints current memory usage stats.
#     See: https://stackoverflow.com/a/15495136

#     :return: None
#     """
#     total, available, percent, used, free = psutil.virtual_memory()
#     total, available, used, free = total / MEGA, available / MEGA, used / MEGA, free / MEGA
#     proc = PROCESS.memory_info()[1] / MEGA
#     print('process = %s total = %s available = %s used = %s free = %s percent = %s'
#           % (proc, total, available, used, free, percent))

def extract_documents(dirn, whitelist):
    ids = []
    docs = []
    print('Reading documents...')
    for i,fname in enumerate(listdir(dirn)):
        fpath = os.path.join(dirn, fname)
        id = fname.split('.txt')[0].split('_')[0]
        # if id not in whitelist :
        #     continue

        ids.append(id)
        doc = []
        with open(fpath) as f :
            doc = f.read().encode('utf-8', errors='replace').decode()
            docs.append(doc)

        if (i+1)%1000==0:
            print(i+1,'/', len(listdir(dirn)), '...')
    return ids,docs

def tokenize_filter(docs) :
    # tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        docs[idx] = re.split(r'\s',docs[idx])  # Split into words.
        if (idx+1)%1000==0:
            print(idx, '/', range(len(docs)))
    return docs

if len(argv) != 6 :
    print("Usage: {} <fulltext_pkl> <abstract_pkl> <dst_dir> <#topics> <seed>\n".format(argv[0]))
    exit(1)

ft_fname = argv[1]
ab_fname = argv[2]
results_dir = argv[3]
num_topics = [ int(i) for i in argv[4].split(',')] #int(argv[4])
random_seed = int(argv[5])

if not os.path.exists(results_dir) :
    print("{} does not exist, exiting...\n".format(results_dir), file=stderr)
    exit(1)

whitelist = set()
with open(os.path.join(results_dir, 'cs_whitelist_3k.txt')) as f :
    for line in f :
        whitelist.add(line.strip())

print("Reading fulltext...")
ids,docs = extract_documents(ft_fname, whitelist)

try:
    with open('./cs_extract_ft_130k','wb') as f:
        pickle.dump([ids,docs],f)
except MemoryError:
    print('memory error')
    # print_memory_usage()

print("Reading abstract...")
ab_ids,ab_docs = extract_documents(ab_fname, whitelist)
try:
    with open('./cs_extract_ab_130k','wb') as f:
        pickle.dump([ab_ids,ab_docs],f)
except MemoryError:
    print('memory error')
    # print_memory_usage()
exit(0)
#with open(ft_fname, 'rb') as f:
#    ids,docs = pickle.load(f) # extract_documents(ft_fname, whitelist)
#print("Reading abstract...")
#with open(ab_fname, 'rb') as f:
#    ab_ids,ab_docs = pickle.load(f) # extract_documents(ab_fname, whitelist)
#print("read", len(docs),"documents")

print("tokenizing...")
docs = tokenize_filter(docs)
ab_docs = tokenize_filter(ab_docs)

print("building dictionary...")
dictionary = Dictionary(docs)
dictionary.filter_extremes()
print('Number of unique tokens: %d' % len(dictionary))

# corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!
# print(corpus_memory_friendly)

corpus = [dictionary.doc2bow(doc) for doc in docs]
ab_corpus = [dictionary.doc2bow(doc) for doc in ab_docs]


# Train LDA model.
chunksize = 2000
passes = 10      # num epoches
iterations = 50   # max passes of E-step
eval_every = None

# Make a index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token



overview = open(results_dir + '/overview.txt', 'w')
print("topics", "coherence", file=overview)

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
        #workers=3
    )

    top_topics = model.top_topics(corpus, docs, dictionary, coherence='c_v', topn=20, processes=4)

    # Average topic coherence 
    avg_topic_coherence = sum([t[1] for t in top_topics]) / t
    print(t, avg_topic_coherence, file=overview)

    with open(results_dir + '/%d_%d_stats.txt' % (t, random_seed), 'w') as f :
        print('Average topic coherence: %.4f.' % avg_topic_coherence, file=f)

    with open(results_dir + '/%d_%d_topics.txt' % (t, random_seed), 'w') as f :
        for ind,top in enumerate(top_topics) :
            print("%d %.4f %s" % (ind, top[1], ','.join([ w for p,w in top[0] ])), file=f)

    topic_dist = model.get_document_topics(corpus)
    with open(results_dir + '/%d_%d_fulltext_composition_compact.txt' % (t, random_seed), 'w') as f :
        for id,d in zip(ids, topic_dist) :
            print(id, ' '.join(["%d=%f" % (tid,prob) for tid,prob in d ]), file=f)

    with open(results_dir + '/%d_%d_fulltext_composition.txt' % (t, random_seed), 'w') as f :
        for id,d in zip(ids, topic_dist) :
            remainder = 0.0 if (len(d) == t) else (1.0 - sum([ prob for _,prob in d ])) / float(t - len(d))
            tmp = dict(d)
            print(id, ' '.join([str(tmp.get(i, remainder)) for i in range(t)]), file=f)

    topic_dist = model.get_document_topics(ab_corpus)
    with open(results_dir + '/%d_%d_abstract_composition_compact.txt' % (t, random_seed), 'w') as f :
        for id,d in zip(ids, topic_dist) :
            print(id, ' '.join(["%d=%f" % (tid,prob) for tid,prob in d ]), file=f)

    # this is always different
    #print(topic_dist[6])

    with open(results_dir + '/%d_%d_abstract_composition.txt' % (t, random_seed), 'w') as f :
        for id,d in zip(ids, topic_dist) :
            remainder = 0.0 if (len(d) == t) else (1.0 - sum([ prob for _,prob in d ])) / float(t - len(d))
            tmp = dict(d)
            print(id, ' '.join([str(tmp.get(i, remainder)) for i in range(t)]), file=f)

overview.close()

