from flask import Flask, render_template, flash, request, redirect, url_for, session, abort, g
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from operator import itemgetter

import numpy as np
import pandas as pd
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import math
import os
import copy

import pygal
import re
import time
import datetime
import pprint as pp
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'


def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


def get_forecasting_val(values):
    look_back = 5
    nepochs = 300
    batch_size = 32

    dataset = copy.deepcopy(values)
    for i in range(len(dataset)):
        dataset[i] = [dataset[i]]
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    train = np.array(dataset)
    trainX, trainY = create_dataset(train, look_back)
    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(4, input_shape=(look_back, 1)))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')
    model.fit(trainX, trainY, epochs=nepochs, batch_size=batch_size, verbose=0)
    
    l = trainX[len(trainX) - 1]
    s = [list(x) for x in l]
    prediction = []
    for it in range(10):
        t = np.array([s])
        pred = model.predict(t)
        predt = scaler.inverse_transform(pred)
        k = []
        for i in range(1, len(s)):
            k.append(s[i])
        k.append(list(pred[0]))
        s = k
        prediction.append(int(predt))
    return prediction

def create_pygraph2(title, g1, g2, l1, l2):
    graph = pygal.Line(height=380, legend_at_bottom=True, legend_at_bottom_columns=2)
    graph.title = title
    graph.add(g1,  l1)
    graph.add(g2,  l2)
    graph_data = graph.render_data_uri()

    return graph_data

def create_pygraph_ar(title, g1, g2, l1, l2):
    graph = pygal.Line(height=380, legend_at_bottom=True, legend_at_bottom_columns=2)
    graph.title = title
    xlabels = [i + 1 for i in range(len(l1))] + [i + 1 + len(l1) for i in range(len(l2))]
    graph.x_labels = xlabels
    ll = []
    for i in range(len(l2)):
        ll.append({'value': l2[i], 'node': {'r': 4}})
    graph.add(g2,  l1 + ll)
    graph_data = graph.render_data_uri()

    return graph_data


@app.route('/', methods=['POST', 'GET', 'PUT', 'DELETE'])
def home():

    data = [60326, 60326, 60511, 60511, 60357, 60347, 60349, 60349, 60349,
       60349, 60349, 60349, 60349, 60349, 60349, 60349, 60349, 60349,
       60329, 60329, 60329, 60329, 60329, 60329, 60112, 61756, 63753,
       63733, 63737, 63737, 63737, 63737, 63737, 63737, 63682]
    # data = [40, 50, 80, 100, 84, 98, 130, 43,
    #                 112, 160, 202, 170, 231, 207, 78,
    #                 250, 277, 291, 89, 315, 300,
    #                 312, 348, 299, 139, 350, 261, 289,
    #                 320, 390, 430, 121, 419, 422, 489,
    #                 467, 560, 390, 650, 623, 730, 722, 570,
    #                 755, 730, 878, 902, 950, 641, 988, 946,
    #                 855, 838, 970, 992, 1050, 751, 1088, 1056]
    #pred = get_forecasting_val(data)
    pred = data + [64111, 64172, 64225, 64257, 64282, 64301, 64315, 64326, 64335, 64341]

    zeros = [0 for x in data]


    graph_arima = create_pygraph2('Forecast', 'Predicion', 'Values', 
                                        pred,
                                        data)
    

    return render_template("home.html", gdata1=graph_arima)


import _thread
import requests


def pooling( threadName, delay):
    url = 'http://194.2.241.244/measure/api/analysis/register'

    token = "my token"
    data = {
            "configurationURL": "http://measure.cs.unibuc.ro:5000",
            "description": "Stracker tool for measure",
            "name": "Stracker"
            }

    headers = {"Content-Type": "application/json", "data":json.dumps(data)}

    response = requests.put(url, data=json.dumps(data), headers=headers)
  
    url = 'http://194.2.241.244/measure/api/analysis/alert/list?id=Stracker'

    while (True):
        time.sleep(1)
        response = requests.get(url)

        al = (response.json())["alerts"]
        
        if len(al) > 0 and al[0]["alertType"] == "ANALYSIS_ENABLE":
            aid = al[0]["properties"][0]["property"]
            proj = al[0]["properties"][0]["value"]

            url2 = 'http://194.2.241.244/measure/api/analysis/configure'

            token = "my token"
            data = {
                    "configurationUrl": "http://measure.cs.unibuc.ro:5000/",
                    "projectAnalysisId": proj,
                    "viewUrl": "http://measure.cs.unibuc.ro:5000/",
                    "cards": [
                        {
                        "cardUrl": "http://measure.cs.unibuc.ro:5000/",
                        "label": "card1",
                        "preferedHeight": 400,
                        "preferedWidth": 300
                        }
                    ]
                    }

            headers = {"Content-Type": "application/json", "data":json.dumps(data)}

            response = requests.put(url2, data=json.dumps(data), headers=headers)



if __name__ == '__main__':
    try:
        _thread.start_new_thread( pooling, ("Thread-1", 2, ) )
    except:
        print ("Error: unable to start thread")
    app.run(host="0.0.0.0")
