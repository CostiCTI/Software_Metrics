'''
    Random Forest Algorithm
'''

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def randomForest(file_name):
    '''
        This function train a model with RandomForestClassifier algorithm from sklearn and
    get the accuracy of the model


    Parameters:
    -----------
    file_name           string, contains the name of the file where we find data for training

    Returns:
    ----------
    accuracy            float, the accuracy of the model
    '''

    # read data from csv and save it in a dataframe
    df = pd.read_csv(file_name)

    # split data into known data and data to predict(target)
    features = list(df.columns[:21])
    results = [df.columns[21]]

    data = df[features]
    target = df[results]

    # split data into train data and test data
    # here we split data in 80% train data and 20% test data
    data_train, data_test, target_train, target_test = train_test_split(data, 
                                                target, test_size=0.20, random_state=42)

    # make a RandomForestClassifier model to apply the Random Forest alogorithm on data
    rfc = RandomForestClassifier(n_estimators=300)

     # fit the model with training data
    rfc.fit(data_train, target_train)

    # get predictions on test data
    prediction = rfc.predict(data_test)

    # get the accuracy of the model
    accuracy = accuracy_score(target_test, prediction) * 100

    return accuracy