from sklearn import linear_model
from sklearn import datasets
import numpy as np
import pandas as pd
import csv

def parseDataOld():
    familyData = [] # list of child lists that will return
    justAttributes = []
    gpaData = []
    gritData = []
    matHardData = []
    with open('train_no_NA.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            familyData.append(row)
    with open('backgroundcopylarger_no_NA.csv') as csvfile:
        bReader = csv.DictReader(csvfile)
        for row in bReader:
            famID = row.get('\ufeffchallengeID')
            for family in familyData:
                familyID = family.get('challengeID')
                #add corresponding background information to appropriate family
                #in familyData by checking ID number
                if famID == familyID:
                    family.update(row)
    return familyData

def parseData():
    trainSet = []
    testSet = []
    familyData = (trainSet,testSet) # list of child lists that will return
    with open('test_linReg.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            testSet.append(row)
    with open('train_no_NA.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            trainSet.append(row)
    with open('backgroundcopylarger_no_NA.csv') as csvfile:
        bReader = csv.DictReader(csvfile)
        for row in bReader:
            famID = float(row.get('\ufeffchallengeID'))
            #separate test and training sets
            for family in testSet:
                testFamID = float(family.get('\ufeffchallengeID'))
                if testFamID > famID:
                    break
                if testFamID == famID:
                    family.update(row)
            for family in trainSet:
                trainFamID = float(family.get('challengeID'))
                #add corresponding background information to appropriate family
                #in familyData by checking ID number
                if trainFamID > famID:
                    break
                if famID == trainFamID:
                    family.update(row)
                    del family['\ufeffchallengeID']
    return familyData

def doReg(trainData,testData):
    X_train = pd.DataFrame(data=trainData).fillna(0)
    print(X_train)
    target = pd.DataFrame(data=trainData, columns=["gpa"]).fillna(0)
    print(target)
    y = target[["gpa"]]
    lm = linear_model.LinearRegression()
    lm.fit(X_train,y)
    #lm.score(X_train,y)
    X_test = pd.DataFrame(data=testData).fillna(0)
    print(X_test)
    predictions = lm.predict(X_test)
    print("gpa predictions")
    print(predictions[0:30])
    target = pd.DataFrame(data=trainData, columns=["grit"]).fillna(0)
    y = target[["grit"]]
    lm.fit(X_train,y)
    predictions = lm.predict(X_test)
    print("grit predictions")
    print(predictions[0:30])

tuple = parseData()
trainData = tuple[0]
testData = tuple[1]

doReg(trainData,testData)

