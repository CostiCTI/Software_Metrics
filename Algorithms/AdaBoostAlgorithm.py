'''
    Decision Tree Algorithm
'''

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score


def adaBoost(data_train, data_test, target_train, target_test):
    '''
        This function train a model with AdaBoostClassifier algorithm from sklearn and
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

    # make a AdaBoostClassifier model to apply the Decision Tree alogorithm on data
    ada_boost = AdaBoostClassifier(n_estimators=100, algorithm='SAMME')

    # fit the model with training data
    ada_boost.fit(data_train, target_train)

    # get predictions on test data
    prediction = ada_boost.predict(data_test)

    # get the accuracy of the model
    accuracy = accuracy_score(target_test, prediction) * 100

    return accuracy