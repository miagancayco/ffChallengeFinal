# given training set data and background data, combine into single children list of
#lists, where each list represents each child
import csv
def parseData():
    childData = [] # list of child lists that will return
    with open('train.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        for r in reader:
            childData.append(r)
    for c in childData:
        print c
    return childData
parseData()
