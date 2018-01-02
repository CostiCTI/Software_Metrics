import numpy as np 
import pandas as pd

from keras.models import Sequential 
from keras.layers import Dense,Activation,Dropout,Lambda 
from keras.layers.normalization import BatchNormalization 
from keras.utils import np_utils
from keras.models import model_from_json

from sklearn.preprocessing import normalize


def save_model(m, file_name):

    model_json = m.to_json()
    with open(file_name + ".json", "w") as json_file:
        json_file.write(model_json)
    m.save_weights(file_name + ".h5")
    
    print ("Model saved!")


def load_model(file_name):

    json_file = open(file_name + ".json", 'r')
    model_json = json_file.read()
    json_file.close()

    m = model_from_json(model_json)
    m.load_weights(file_name + ".h5")

    print("Model loaded!")
    return m


#Read data from csv file 
df = pd.read_csv("../data/set.csv")

df.loc[df["problems"] == False, "problems"] = 0
df.loc[df["problems"] == True,  "problems"] = 1

df = df.iloc[np.random.permutation(len(df))]

#split data into training features and and target features 
data = df.iloc[:,0:21].values
target = df.iloc[:,21].values

nor_data = normalize(data, axis=0)

# split data into training data and testing data
l = len(df)
l_train = int(0.8 * l)
l_test  = int(0.2 * l)

data_train = nor_data[:l_train]
data_test  = nor_data[l_train:]

target_train = target[:l_train]
target_test  = target[l_train:]

# Transform target in one hot vector (to use softmax)
# 0 become [1 0]
# 1 become [0 1]
target_train = np_utils.to_categorical(target_train, num_classes=2)
target_test  = np_utils.to_categorical(target_test, num_classes=2)


model = Sequential()

model.add(Dense(2000,input_dim=21,activation='relu'))
model.add(Dense(1000,activation='relu'))
model.add(Dense(500,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(2,activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.fit(data_train,target_train,validation_data=(data_test,target_test),batch_size=10,epochs=600,verbose=1)

save_model(model, "m2")

# check accuracy
pred = model.predict(data_test)
size = len(pred)
y       = np.argmax(target_test, axis=1)
predict = np.argmax(pred, axis=1)

accuracy = np.sum(y == predict) / size * 100
print ("Accuracy: ", accuracy )


#load model and check accuracy
new_model = load_model('m2')

pred = new_model.predict(data_test)
size = len(pred)
y       = np.argmax(target_test, axis=1)
predict = np.argmax(pred, axis=1)

accuracy = np.sum(y == predict) / size * 100
print ("Accuracy: ", accuracy )


