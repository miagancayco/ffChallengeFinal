#does kNN on our data
# (c) 2018 Alex C. Taylor

import csv
import math

#merges the train and background tables into one
def makeTable():
    trainingSet = []
    with open('train.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter= ',')
        for r in reader:
            trainingSet.append(r)
    with open('background.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter= ',')
        tIndex = 0
        for r in reader:
            if(tIndex < len(trainingSet) and r[0] == trainingSet[tIndex][0]):
                trainingSet[tIndex].append(r)
                tIndex += 1
    for t in trainingSet:
        print t
    return trainingSet

#do the kNN

makeTable()
