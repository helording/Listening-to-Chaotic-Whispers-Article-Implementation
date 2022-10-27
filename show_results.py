import pickle
import matplotlib.pyplot as plt
import numpy as np
import h5py

from keras.models import Model
from keras.layers import Dense, Input, Activation, multiply, Lambda
from keras.layers import TimeDistributed, GRU, Bidirectional, LSTM
from keras import backend as K
import os
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical

def han():
# refer to 4.2 in the paper whil reading the following code

    # Input for one day : max article per day =40, dim_vec=200
    input1 = Input(shape=(40, 200), dtype='float32')

    # Attention Layer
    dense_layer = Dense(200, activation='tanh')(input1)
    softmax_layer = Activation('softmax')(dense_layer)
    attention_mul = multiply([softmax_layer,input1])
	#end attention layer
    vec_sum = Lambda(lambda x: K.sum(x, axis=1))(attention_mul)
    pre_model1 = Model(input1, vec_sum)


    pre_model2 = Model(input1, vec_sum)

    # Input of the HAN shape (None,11,0,200)
	# 11 = Window size = N in the paper 40 = max articles per day, dim_vec = 200
    input2 = Input(shape=(11, 10, 200), dtype='float32')

    # TimeDistributed is used to apply a layer to every temporal slice of an input
	# So we use it here to apply our attention layer ( pre_model ) to every article in one day
	# to focus on the most critical article
    pre_gru = TimeDistributed(pre_model1)(input2)

	# bidirectional gru
    l_gru = Bidirectional(GRU(100, return_sequences=True))(pre_gru)

	# We apply attention layer to every day to focus on the most critical day
    post_gru = TimeDistributed(pre_model2)(l_gru)

    # MLP to perform classification
    dense1 = Dense(100, activation='tanh')(post_gru)
    dense2 = Dense(3, activation='tanh')(dense1)
    final = Activation('softmax')(dense2)
    final_model = Model(input2, final)
    final_model.summary()

    return final_model

def open_pickle(url):
    with open(url, 'rb') as file:
        return pickle.load(file)


def open_numpy(url):
    with open(url, 'rb') as file:
        f = np.load(file)
        return f


def create_article_list(dic_file, nb_article=362):
    dic = sorted(dic_file.items(), reverse=True)
    articles = []
    for i in dic:
        if nb_article > 0:
            articles.append([i[0], i[1]])
            nb_article -= 1
    return articles


def compute_accuracy(real_value, prediction):
    ech_len = len(real_value)
    errors = 0
    assert len(real_value) == len(prediction)
    for i, j in enumerate(real_value):
        if real_value[i] != prediction[i]:
            errors += 1
    if ech_len > 0:
        return (errors/ech_len)*100
    else:
        return


def plot_data(company, real_value, prediction, accuracy):
    assert len(real_value) == len(prediction)
    fig, ax = plt.subplots()
    fig.suptitle(company + " GRU")
    y = []
    y_pred = []
    for i in range(0, len(real_value)):
        y.append(real_value[i])
        y_pred.append(prediction[i])
    x = np.arange(0, len(real_value), 1)
    ax.set_title('Accuracy = ' + str(accuracy) + " %")
    ax.set_xlabel("Days")
    ax.set_ylabel("Variation of stock prices")
    ax.plot(x, y, label='real')
    ax.plot(x, y_pred, label='predicted')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    '''
    Amazon
    Wells Fargo
    Visa
    T-Mobile
    '''
    company = "T-Mobile"
    x_test_file = "x_test/"+ str(company)+"_x_test.npy"
    y_test_file = "y_test/"+ str(company)+"_y_test.npy"
    x_test = np.load(x_test_file)
    y_test = np.load(y_test_file)
    model = han()
    model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])
    model.load_weights('GRU10epochs.hdf5')


    #f = open_pickle('./pickle_article/Amazon.csv.pkl')
    #articles_list = create_article_list(f)
    #share_price = open_pickle('./pickle/Amazon.pkl')

    #share_price_value = [share_price[i[0]] for i in articles_list]
    share_price_value = np.load(y_test_file)

    #model_prediction_share_price = open_numpy('./Amazon_y_test.npy')
    model_prediction_share_price = model.predict(x_test)
    #print(model_prediction_share_price)
    model_prediction_share_price_normalize = []
    for i in model_prediction_share_price:
        print(i)
        max = np.max(i)
        if i[0] == max:
            model_prediction_share_price_normalize.append(-1)
        elif i[1] == max:
            model_prediction_share_price_normalize.append(0)
        else:
            model_prediction_share_price_normalize.append(1)

    actualValues = []
    for price in share_price_value:
        if price[0] == 1:
            actualValues.append(-1)
        elif price[1] == 1:
            actualValues.append(0)
        else:
            actualValues.append(1)


    share_price_value = actualValues
    print("\nMODEL PREDICT NORMALIZED")
    print(model_prediction_share_price_normalize)
    print("\n")
    print(share_price_value)
    #print(share_price_value)
    print("Accuracy = ", str(compute_accuracy(share_price_value, model_prediction_share_price_normalize)) + " %")
    plot_data(company, share_price_value, model_prediction_share_price_normalize, compute_accuracy(share_price_value, model_prediction_share_price_normalize))
