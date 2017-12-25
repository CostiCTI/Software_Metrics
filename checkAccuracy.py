'''
    This script runs all algorithms and saves the results in a json file
'''
import json

import DecisionTreeAlgorithm as dt
import RandomForestAlgorithm as rf
import SVMAlgorithm as svm

FILE_NAME = 'data/metrics_set.csv'
DESTINATION_FILE = 'results.json'

def main():

    dtAccuracy  = dt.decisionTree(FILE_NAME)
    rfAccuracy  = rf.randomForest(FILE_NAME)
    svmAccuracy = svm.SVMClassification(FILE_NAME)

    accuracyDict = {}
    accuracyDict['DecisionTree'] = dtAccuracy
    accuracyDict['RandomForest'] = rfAccuracy
    accuracyDict['SVM'] = svmAccuracy

    with open(DESTINATION_FILE, 'w') as data_file:
        json.dump(accuracyDict, data_file, indent=4, sort_keys=True)

if __name__ == '__main__':

    main()

