#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from sys import exit, argv, stderr
import os.path
import re, pickle
from os import listdir
from paths import data_path

from nltk.tokenize import RegexpTokenizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel,LdaMulticore


def extract_documents(dirn, whitelist):
    ids = []
    docs = []
    print('Reading documents...')
    for i,fname in enumerate(listdir(dirn)[:100]):
        fpath = os.path.join(dirn, fname)
        id = fname.split('.txt')[0].split('_')[0]
        if id not in whitelist :
            continue

        ids.append(id)
        doc = []
        with open(fpath) as f :
            doc = f.read().encode('utf-8', errors='replace').decode()
            doc = doc.split('\n')
            # for line in f :
                # line = line.strip()
                # if not line : 
                #     continue
                # line = line.encode('utf-8', errors='replace').decode()
                # id,line = line.split(" ", 1)
            docs.append(doc)

        if (i+1)%1000==0:
            print(i+1,'/', len(listdir(dirn)), '...')
    return ids,docs

if len(argv) != 6 :
    print("Usage: {} <fulltext_dir> <abstract_dir> <dst_dir> <#topics> <seed>\n".format(argv[0]))
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
with open(os.path.join(data_path, 'cs_whitelist_3k.txt')) as f :
    for line in f :
        whitelist.add(line.strip())

ids,docs = extract_documents(ft_fname, whitelist)
ab_ids,ab_docs = extract_documents(ab_fname, whitelist)
print("read", len(docs),"documents")

with open(os.path.join(data_path,'cs_extract_ft.pkl'), 'wb') as f:
    pickle.dump([ids,docs],f)
with open(os.path.join(data_path,'cs_extract_ab.pkl'), 'wb') as f:
    pickle.dump([ab_ids, ab_docs],f)
exit(0)

print("building dictionary...")
dictionary = Dictionary(docs) # os.path.join(data_path, 'cs_dict.pkl')
print('Number of unique tokens: %d' % len(dictionary))
# dictionary.save('./cs_dict.pkl')

corpus = [dictionary.doc2bow(doc) for doc in docs]
# with open(os.path.join(data_path,'ft_corpus.pkl'), 'rb') as f:
#     corpus = pickle.load(f, encoding='utf-8', errors='ignore')

ab_corpus = [dictionary.doc2bow(doc) for doc in ab_docs]
# with open(os.path.join(data_path,'ab_corpus.pkl'), 'rb') as f:
#     ab_corpus = pickle.load(f, encoding='utf-8', errors='ignore')

# ids, docs= [fname.split('.txt')[0].split('_')[0] for fname in listdir(ft_fname)], [dictionary.bow for bow in corpus]
# ab_ids, ab_docs = [fname.split('.txt')[0].split('_')[0] for fname in listdir(ab_fname)], [bow.get_texts() for bow in ab_corpus]

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

    model = LdaMulticore(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        #alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=t,
        passes=passes,
        eval_every=eval_every,
        random_state=random_seed,
        workers=3
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

