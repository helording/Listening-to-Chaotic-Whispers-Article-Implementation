from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import os
import numpy as np
import nltk

class OurDoc2Vec(object):


    def __init__(self, dirname, model_path):

        self.dirname = dirname
        self.model_path = model_path
        self.tagged_data = []

    def prepare_data(self):

        data = []
        tag = []
        i = 0

		# simple for loops to get all the articles and add them to the data and tag list
        for newspaper in os.listdir(self.dirname):
            days = os.path.join(self.dirname, newspaper)
            if "DS_Store" in days:
                continue
            if i is 10:
                break
            for day in os.listdir(days):
                day_path = os.path.join(days, day)
                if "DS_Store" in day_path:
                    continue
                if i is 10:
                    break
                for fname in os.listdir(day_path):
                    if "DS_Store" in fname:
                        continue
                    f_path = os.path.join(day_path, fname)
                    print(f_path)
                    data.append(open(f_path, 'rb').read())
                    print("THIS TAG IS IN " + str(fname[:-4]))
                    tag.append(fname[:-4])
                    print(i)
                    i += 1
                    if i is 10:
                        break

		# tagging all the articles
        self.tagged_data = [TaggedDocument(words=word_tokenize(str(_d.lower())), tags=[str(tag[i])]) for i, _d in
                            enumerate(data)]

        # Freeing memory

        data = []
        tag = []

    def train_doc2vec(self, max_epochs=15, vec_size=200, alpha=0.025):

        model = Word2Vec(size=200, alpha=alpha, window=5, min_count=1, workers=30)

        model.build_vocab(self.tagged_data)


        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(self.tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # decrease learning rate
            model.alpha -= 0.0002
            # and reinitialize it
            model.min_alpha = model.alpha

        model.save(self.model_path)
        print("Model savec")

    def clean_train_model(self):

        """
		Aims at using the model trainned by first deleting the temporary training data. Use it carefully you can lose all the progress made in the training.
        :return:s
        """

        model = Word2Vec.load(self.model_path)
        # Be careful here
        model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    def test_doc2vec(self):

        """
        To test the  model
        :return:

        """
        model = Word2Vec.load(self.model_path)

        model.docvecs.doctags

        # to print the vectorized article using tags
        vector = model.docvecs['0000_38']
        print(type(vector))
        print("Vector of document:", vector)

    def readFile(self):

        """
        To read the files created by doc2vec model
        :return:
        """

        model = Word2Vec.load(self.model_path)

        print(type(model.docvecs.doctags))

        file = np.load('/Users/admin/Dropbox/School work/SJTU/AIProject/Listening-to-Chaotic-Whishpers--Code-master/doc2vec/d2v.model.docvecs.vectors_docs.npy')

        fil2 = np.load('/Users/admin/Dropbox/School work/SJTU/AIProject/Listening-to-Chaotic-Whishpers--Code-master/doc2vec/d2v.model.trainables.syn1neg.npy')

        file3 = np.load('/Users/admin/Dropbox/School work/SJTU/AIProject/Listening-to-Chaotic-Whishpers--Code-master/doc2vec/d2v.model.wv.vectors.npy')


        print(file3)

def test_doc2vec():

    """
    To test the  model
    :return:

    """
    model = Doc2Vec.load('./d2v.model')

    model.docvecs.doctags

    # to print the vectorized article using tags
    vector = model.docvecs['0000_38']
    print(type(vector))
    print("Vector of document:", vector)

if __name__ == '__main__':
    nltk.download('punkt')
    model = OurDoc2Vec("/Users/admin/Dropbox/School work/SJTU/AIProject/Listening-to-Chaotic-Whishpers--Code-master/text_data/", "./d2v.model")
    model.prepare_data()
    model.train_doc2vec()
    model.test_doc2vec()
    model = Word2Vec.load('./d2v.model')

    test_doc2vec()
    #model.readFile()
