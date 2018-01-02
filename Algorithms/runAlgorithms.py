'''
    This script runs all algorithms and saves the results in a json file
'''
import json

import DecisionTreeAlgorithm as dt
import RandomForestAlgorithm as rf
import SVMAlgorithm as svm
import KNNAlgorithm as knn
import LogisticRegAlgorithm as logr

FILE_NAME = '../data/set.csv'
DESTINATION_FILE = 'results.json'

def main():

    dtAccuracy   = dt.decisionTree(FILE_NAME)
    rfAccuracy   = rf.randomForest(FILE_NAME)
    svmAccuracy  = svm.SVMClassification(FILE_NAME)
    knnAccuracy  = knn.KNNClassification(FILE_NAME)
    logrAccuracy = logr.logisticReg(FILE_NAME)

    accuracyDict = {}
    accuracyDict['DecisionTree'] = round(dtAccuracy, 2)
    accuracyDict['RandomForest'] = round(rfAccuracy, 2)
    accuracyDict['SVM'] = round(svmAccuracy, 2)
    accuracyDict['KNN'] = round(knnAccuracy, 2)
    accuracyDict['LogisticRegression'] = round(logrAccuracy, 2)

    with open(DESTINATION_FILE, 'w') as data_file:
        json.dump(accuracyDict, data_file, indent=4, sort_keys=True)

if __name__ == '__main__':

    main()

