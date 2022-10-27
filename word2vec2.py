from keras.layers import Embedding, merge, Concatenate, concatenate
from keras.engine import Input
from keras.models import Model
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import os
import json
import numpy as np
import time

tokenize = lambda x: simple_preprocess(x)


class SentenceGenerator(object):

    def __init__(self, dirname):

        self.dirname = dirname

    def __iter__(self):



        i = 0
        for newspaper in os.listdir(self.dirname):
            if "DS_Store" in newspaper:
                continue
            days = os.path.join(self.dirname, newspaper)
            for day in os.listdir(days):
                if "DS_Store" in day:
                    continue
                day_path = os.path.join(days, day)
                for fname in os.listdir(day_path):
                    if "DS_Store" in fname:
                        continue
                    f_path = os.path.join(day_path, fname)
                    print(f_path)
                    print(i)
                    i += 1
                    for line in open(f_path, 'rb'):
                        yield tokenize(line)


def create_embeddings(data_dir, embeddings_path, vocab_path, **params):

    i = 0
    vv = []
    for newspaper in os.listdir(data_dir):
        if "DS_Store" in newspaper:
            continue
        days = os.path.join(data_dir, newspaper)
        for day in os.listdir(days):
            if "DS_Store" in day:
                continue
            day_path = os.path.join(days, day)
            for fname in os.listdir(day_path):
                if "DS_Store" in fname:
                    continue
                f_path = os.path.join(day_path, fname)
                print(f_path)
                print(i)
                i += 1
                for line in open(f_path, 'rb'):
                    ll = tokenize(line)
                    #print(ll)
                    vv[2:2] = ll
                    #print("vv is now " + str(vv))
                    #time.sleep(1)


    model = Word2Vec(vv, **params)
    weights = model.wv.syn0
    np.save(open(embeddings_path, 'wb'), weights)

    vocab = dict([(k, v.index) for k, v in model.wv.vocab.items()])
    with open(vocab_path, 'w') as f:
        f.write(json.dumps(vocab))


def load_vocab(vocab_path):
    with open(vocab_path, 'r') as f:
        data = json.loads(f.read())
    word2idx = data
    idx2word = dict([(v, k) for k, v in data.items()])
    return word2idx, idx2word


def word2vec_embedding_layer(embeddings_path):
    weights = np.load(open(embeddings_path, 'rb'))
    layer = Embedding(input_dim=weights.shape[0], output_dim=weights.shape[1], weights=[weights])
    return layer


if __name__ == '__main__':

    data_path = ['text_data/',
                 'weights',
                 'vocab']

    # variable arguments are passed to gensim's word2vec model
    #create_embeddings(data_path[0], data_path[1], data_path[2], size=300, min_count=5,
    #                  window=10, sg=1, iter=15)

    word2idx, idx2word = load_vocab(data_path[2])

    # cosine similarity model
    print(word2idx)

    model = Word2Vec(word2idx, min_count=1)
    v1 = word2vec.wv['company']

    while True:
        word_a = input('First word: ')
        if word_a not in word2idx:
            print('Word "%s" is not in the index' % word_a)
            continue
        word_b = input('Second word: ')
        if word_b not in word2idx:
            print('Word "%s" is not in the index' % word_b)
            continue
        output = model.predict([np.asarray([word2idx[word_a]]),
                                np.asarray([word2idx[word_b]])])
        print(output)
