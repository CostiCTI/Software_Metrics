'''
    Random Forest Algorithm
'''

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def randomForest(data_train, data_test, target_train, target_test):
    '''
        This function train a model with RandomForestClassifier algorithm from sklearn and
    get the accuracy of the model


    Parameters:
    -----------
    data_train          numpy.array, data for training
    data_test           numpy.array, data for testing 
    target_train        numpy.array, target for training set(the same length as data_train)
    target_test         numpy.array, target for testing set(the same length as data_test)

    Returns:
    ----------
    accuracy            float, the accuracy of the model
    '''

    # make a RandomForestClassifier model to apply the Random Forest alogorithm on data
    rfc = RandomForestClassifier(n_estimators=30)

     # fit the model with training data
    rfc.fit(data_train, target_train.ravel())

    # get predictions on test data
    prediction = rfc.predict(data_test)

    # get the accuracy of the model
    accuracy = accuracy_score(target_test, prediction) * 100

    return accuracy


