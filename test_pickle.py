import pickle
import os


def test_pickle(path):

    if os.path.getsize(article) > 0:
        with open(article, 'rb') as handle:
            unpickler = pickle.Unpickler(handle)
            b = unpickler.load()
    print(b)


if __name__ == '__main__':
    article = '/home/zeninvest/firm_csv_folder/pickle/3M.csv.pkl'
    test_pickle(article)

