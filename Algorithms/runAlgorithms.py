'''
    This script runs all algorithms and saves the results in a json file
'''
import json
import numpy as np
import pandas as pd

import DecisionTreeAlgorithm as dt
import RandomForestAlgorithm as rf
import SVMAlgorithm as svm
import KNNAlgorithm as knn
import LogisticRegAlgorithm as logr
import GradientBoostAlgorithm as gb
import AdaBoostAlgorithm as ab

from sklearn.cross_validation import train_test_split

FILE_NAME = '../data/promise/complete_set.csv'
DESTINATION_FILE = 'results.json'


def prepareData(file_name):

    # read data from csv and save it in a dataframe
    df = pd.read_csv(file_name)

    #df = df.drop('name', 1)
    #df = df.drop('version', 1)
    #df = df.drop('namep', 1)

    df.bug[df.bug == 0] = 0 
    df.bug[df.bug != 0] = 1 

    #df.to_csv('../data/promise/CK.csv', index=False)

    num_columns = len(df.columns)

    # split data into known data and data to predict(target)
    features = list(df.columns[:num_columns - 1])
    results = [df.columns[num_columns - 1]]

    data = df[features]
    target = df[results]

    # split data into train data and test data
    # here we split data in 80% train data and 20% test data
    data_train, data_test, target_train, target_test = train_test_split(data, 
                                                target, test_size=0.20, random_state=42)

    # transform dataframe into numpy.array
    data_train = data_train.values
    data_test  = data_test.values
    target_train = target_train.values
    target_test  = target_test.values



    return [data_train, data_test, target_train, target_test]


def main():

    data_list = prepareData(FILE_NAME)


    print ('Decision Tree...')
    dtAccuracy   = dt.decisionTree(data_list[0], data_list[1], data_list[2], data_list[3])
    print ('Random Forest...')
    rfAccuracy   = rf.randomForest(data_list[0], data_list[1], data_list[2], data_list[3])
    print ('SVM...')
    svmAccuracy  = svm.SVMClassification(data_list[0], data_list[1], data_list[2], data_list[3])
    print ('KNN...')
    knnAccuracy  = knn.KNNClassification(data_list[0], data_list[1], data_list[2], data_list[3])
    print ('Logistic Reg...')
    logrAccuracy = logr.logisticReg(data_list[0], data_list[1], data_list[2], data_list[3])
    print ('Gradient Boost')
    gbAccuracy   = gb.gradientBoost(data_list[0], data_list[1], data_list[2], data_list[3])
    print ('Ada Boost')
    abAccuracy   = ab.adaBoost(data_list[0], data_list[1], data_list[2], data_list[3])

    accuracyDict = {}
    accuracyDict['DecisionTree']       = round(dtAccuracy, 2)
    accuracyDict['RandomForest']       = round(rfAccuracy, 2)
    accuracyDict['SVM']                = round(svmAccuracy, 2)
    accuracyDict['KNN']                = round(knnAccuracy, 2)
    accuracyDict['LogisticRegression'] = round(logrAccuracy, 2)
    accuracyDict['GradientBoost']      = round(gbAccuracy, 2)
    accuracyDict['AdaBoost']           = round(abAccuracy, 2)

    with open(DESTINATION_FILE, 'w') as data_file:
        json.dump(accuracyDict, data_file, indent=4, sort_keys=True)


if __name__ == '__main__':

    main()

