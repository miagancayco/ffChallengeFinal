from sklearn import linear_model
from sklearn import datasets
import numpy as np
import pandas as pd
import csv

def parseData():
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

def doReg(data):
    df = pd.DataFrame(data=data).fillna(0)
    print(df)
    target = pd.DataFrame(data=data, columns=["gpa"]).fillna(0)
    print(target)
    X = df
    #print(X)
    y = target[["gpa"]]
    lm = linear_model.LinearRegression()
    model = lm.fit(X,y)
    predictions = lm.predict(X)
    print("gpa predictions")
    print(predictions[0:30])
    target = pd.DataFrame(data=data, columns=["grit"]).fillna(0)
    y = target[["grit"]]
    model = lm.fit(X,y)
    predictions = lm.predict(X)
    print("grit predictions")
    print(predictions[0:30])

data = parseData()

doReg(data)

