import pickle as _pickle
import pickle
import numpy as np
from gensim.models.doc2vec import Doc2Vec
from sklearn.model_selection import train_test_split
import os
import multiprocessing as mp
import time
from sentence_transformers import SentenceTransformer


def create_x_y(name, model, firm_article, firm_stock, k_max=40, test_size=0.33, window=10):

    notTagged = 1;
    # opening the pickle for article dictionnary
    try:
        with open(firm_article, 'rb') as dict_article:
            dico_article = pickle.load(dict_article)
    except OSError as e:
        print("CANT OPENNNNN " + str(firm_article))

    # opening pickle for stock trend dictionnary
    try:
        with open(firm_stock, 'rb') as dict_stock:
            dico_stock = pickle.load(dict_stock)
    except OSError as e:
        print("CANT OPENNNNN " + str(firm_stock))

    # check if both dict are non empty
    if (len(dico_article) > 0) and (len(dico_stock) > 0):

        # creating the array
        data = np.zeros((1, 11, k_max, 200), dtype='float32')

        y = []
        dates = []

        for i in range(int(1095)):
            #print(i)
            # bool to know if any article was puslihed during the 11 days
            to_add = False
            # we want to predict the trend on day i+1, so we check if day i+1 is actually a key in dico_stock dictionnary
            # change from i + 1 to 1 because of line up problems
            next_day_key = str(i).zfill(4)
            if next_day_key in dico_stock:
                y_i = int(dico_stock[next_day_key])
                # new row to add to the data array
                new_row = np.zeros((1, 11, k_max, 200), dtype='float32')
                for j in range(11):
                    # we look from i-k_max to i
                    day_key = str(i - j).zfill(4)
                    #print(day_key)
                    if (day_key in dico_article):
                        list_article = dico_article[day_key]
                        to_add = True
                        # k= key, x=value=list of ID of articles of that day
                        for k in range(k_max):
                            if k < len(dico_article[day_key]):
                                article_id = list_article[k]
                                #print("article_id: " + str(article_id))
                                try:

                                    article_id = list_article[k]
                                    vector = model.docvecs[article_id]
                                    new_row[0, j, k, :] = vector
                                    print("SUCCESSFUL TAGGED: " + str(article_id))
                                except KeyError as k:
                                    print("article " + str(article_id) + " not tagged #" + str(notTagged))
                                    continue
                                new_row[0, j, k, :] = vector[:200]
                            else:
                                new_row[0, j, k, :] = np.zeros(200)

                if to_add:
                    # we add the line
                    data = np.vstack([data, new_row])
                    y.append(y_i)
                    dates.append(next_day_key)

        y_vec = np.asarray(y)
        x_mat = np.delete(data, (0), axis=0)  # deletes the first line full of zeros
        x_train, x_test, y_train, y_test = train_test_split(
            x_mat, y_vec, test_size=test_size, random_state=42, shuffle=False)

        y_train_size = y_train.shape[0]
        dates_test = dates[y_train_size:]

        with open('/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/dates/dates' + name + '.pkl', 'wb+') as handle:
            pickle.dump(dates_test, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return (x_train, x_test, y_train, y_test)
    else:
        print("Error File")
        return [], [], [], []


def create_dataset(stockfile_list, articlefile_list):


    # check if we have the same number of companies for day in os.listdir(dirname):
    print(len(os.listdir(stockfile_list)))
    print(len(os.listdir(articlefile_list)))
    listPrice = os.listdir(stockfile_list)
    listArt = os.listdir(articlefile_list)

    notIn = []

    for art in listArt:
        print(art[:-8])
        #found = False
        for price in listPrice:

            if art[:-8] in price:
                found = True
                break
            else:
                found = False

        if found is False:
            notIn.append(art)
            print("adding: " + str(art))

    print(len(os.listdir(stockfile_list)))
    print(len(os.listdir(articlefile_list)))

    #assert len(os.listdir(stockfile_list)) == len(os.listdir(articlefile_list))

    # loading d2v model

    stockfile_list = os.listdir(stockfile_list)
    articlefile_list = os.listdir(articlefile_list)
    model = Doc2Vec.load('./d2v.model')

    for i, stock in enumerate(stockfile_list):
        for z,art in enumerate(articlefile_list):
            if art[:-8] not in stock:
                continue
            elif "DS_Store" in art:
                continue
            # get the name of firm and delete the file extension
            name = articlefile_list[z][:-8]

            try:
                x_train, x_test, y_train, y_test = create_x_y(name, model, './pickle_article/' + articlefile_list[z],
                                                              './pickle/' + stockfile_list[i], 10, 0.33, 10)
            except _pickle.UnpicklingError:
                print("PICKLE ERROR")
                continue

            if len(x_train) > 0:

                # Encoding y_test to have 3 dimension ( to perfom 3 class classification )
                y_test_encode_start = list()
                for trend in y_test:
                    new_value = trend + 1
                    code = [0 for _ in range(3)]
                    code[new_value] = 1
                    y_test_encode_start.append(code)
                y_test_encode_end = np.asarray(y_test_encode_start)

                sleep(10)

                # Create numpy files
                print("======= SAVING ========")
                np.save('./x_train/' + name + '_x_train.npy', x_train)
                np.save('./x_test/' + name + '_x_test.npy', x_test)

                np.save('./y_train/' + name + '_y_train.npy', y_train)
                np.save('./y_test/' + name + '_y_test.npy', y_test_encode_end)

            # Counts iteration
            nb_iteration = len(stockfile_list) - i

if __name__ == "__main__":
    create_dataset('./pickle', './pickle_article')
