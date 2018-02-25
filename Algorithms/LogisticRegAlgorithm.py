'''
    Logistic Regression Algorithm
'''

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def logisticReg(data_train, data_test, target_train, target_test):
    '''
        This function train a model with LogisticRegression algorithm from sklearn and
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

    # make a LogisticRegression model to apply the Decision Tree alogorithm on data
    log_reg_model = LogisticRegression()

    # fit the model with training data
    log_reg_model.fit(data_train, target_train)

    # get predictions on test data
    prediction = log_reg_model.predict(data_test)

    # get the accuracy of the model
    accuracy = accuracy_score(target_test, prediction) * 100

    return accuracy
