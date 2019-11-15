from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.wrappers import LdaMallet

# def 

if __name__ == "__main__":
    p2mallet = '/home/yzan/Desktop/mallet-2.0.8/bin/mallet'
    model = LdaMallet(p2mallet, corpus=common_corpus, num_topics=20, id2word=common_dictionary)
    vector = model[common_corpus[0]]
    print()