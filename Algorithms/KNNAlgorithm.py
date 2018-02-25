'''
    KNN Algorithm
'''

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def KNNClassification(data_train, data_test, target_train, target_test):
    '''
        This function train a model with KNN algorithm from sklearn and
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

    # make a KNN model (k = 25)
    knn = KNeighborsClassifier(n_neighbors=25)

    # fitting the model
    knn.fit(data_train, target_train.ravel())

    # get predictions
    prediction = knn.predict(data_test)

    # get accuracy
    accuracy = accuracy_score(target_test, prediction) * 100

    return accuracy