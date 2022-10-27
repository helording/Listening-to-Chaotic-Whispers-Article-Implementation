from keras.models import Model
from keras.layers import Dense, Input, Activation, multiply, Lambda
from keras.layers import TimeDistributed, GRU, Bidirectional, LSTM
from keras import backend as K
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical


def han():
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


def load_data(model, x_train_file, x_test_file, y_train_file, y_test_file):
    '''
    x_train = np.load(x_train_file)
    y_train = np.load(y_train_file)
    '''
    x_test = np.load(x_test_file)
    y_test = np.load(y_test_file)

    '''
    encoder = LabelEncoder()
    encoder.fit(y_train)
    encoded_Y = encoder.transform(y_train)
    y_train_end = to_categorical(encoded_Y)


    encoder2 = LabelEncoder()
    encoder.fit(y_test)
    encoded_Y2 = encoder.transform(y_test)
    y_test_end = to_categorical(encoded_Y2)
    print(y_test_end.shape)
    '''


    print("model compiling - Hierachical attention network")

    model = han()
    model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])
    model.load_weights('your_model_60epochs.hdf5')

    '''
    print("model fitting - Hierachical attention network")

    print(x_train.shape, y_test_end.shape)

    model.fit(x_train, y_train_end, epochs=200)
    '''


    final_x_test_predict = model.predict(x_test)

    print("Prediction Y ", final_x_test_predict)
    print("Test Y ", y_test)

    return





def twin_creation( x_train_folder, y_train_folder) :


	x_train_list= os.listdir(x_train_folder)
	x_train_list=sorted(x_train_list)

	y_train_list=os.listdir(y_train_folder)
	y_train_list=sorted(y_train_list)

	duo_list=[]
	for i in range ( len(y_train_list) ):
		duo=[x_train_list[i],y_train_list[i]]
		duo_list.append(duo)

	return duo_list

def training(x_name,y_name,model):
    x_train = np.load('./x_train/'+x_name)
    y_train = np.load('./y_train/'+y_name)

    y_oh_list=[] # y one hot for one hot encoding

	# Transforming Y so that it has 3 dim for a 3 class classification
    for trend in y_train:
        new_value=trend+1
        code = [0 for _ in range(3)]
        code[new_value]=1
        y_oh_list.append(code)

    y_train_end=np.asarray(y_oh_list)
    print(y_train_end.shape)

    model.train_on_batch(x_train, y_train_end)
    print("model fitting on "+x_name)

if __name__ == "__main__":

    model = han()
    model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

    #model.load_weights('your_model_60epochs.hdf5')

    x_train_folder = 'x_train'
    y_train_folder = 'y_train'
    epochs=10

    duo_list = twin_creation( x_train_folder, y_train_folder)
    for epoch in range(epochs):
    	for k,duo in enumerate(duo_list):
    	    print('fitting on firm nb {} out of 494 epoch {}'.format(k,epoch))
    	    training(duo[0],duo[1],model)
    	epoch += 1

    model.save('GRU{}epochs.hdf5'.format(epochs))

    #load_data(None, None, "x_test/Amazon_x_test.npy", None, "y_test/Amazon_y_test.npy")

    #np.save('./y_train/' + name + '_y_train.npy', y_train)
    #np.save('./y_test/' + name + '_y_test.npy', y_test_encode_end)

#load_data(model, '', '', '', '')
