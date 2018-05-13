import csv
#given training set data and background data, combine into single list of
#data on all children
def parseData():
    familyData = [] # list of child lists that will return
    with open('train.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            familyData.append(row)
            print row
    with open('background.csv') as csvfile:
        bReader = csv.DictReader(csvfile)
        for row in bReader:
            famID = row.get('challengeID')
            for family in familyData:
                familyID = family.get('challengeID')
                #add corresponding background information to appropriate family
                #in familyData by checking ID number
                if famID == familyID:
                    family.update(row)
    return familyData

def addIfNeighbor(possibleNeighbor, ansInCommon, childToClassify, k, neighbors, minChild, minCt):
    #in case where current number of neighbors is not k, do not need to check and
    #see if need to add new neighbor and remove old neighbor
    if len(neighbors) < k:
        neighbors.append(possibleNeighbor)
    elif ansInCommon > minCt:
        neighbors.append((ansInCommon, possibleNeighbor)) # fix so that append with count
        neighbors.remove((minCt,minChild))
        minChild = resetMin(neighbors) # check if this line works
    return

#walk down list of k neighbors, find new min child, and reset pointer
def resetMin(neighbors):
    result = neighbors[0]
    minCt = neighbors[0][1]
    for n in neighbors:
        if n[1] < minCt:
            result = n
            minCt = n[1]
    return result

#return number of answers have in common
def countAnsInCommon(childA, childB):
    commonAns = 0
    #iterating through all answers in child data and counting all answers have in common
    for i in range(0, len(childA)): #note: adjust so make sure that skip over parts of list that have to do with classifications
        if childB[i] == childA[i]:
            commonAns += 1
    return commonAns
#given family survey data, group questions according to which year asked
def groupByYear(year):
    return

#given list of data on all children, parse through data, select subset according
#to sorting function; run kNN on subset in order to classify given child
def kNNClassifySubsection( sortByFn, child, childData, k ):
    neighbors = []
    currentMinChild = none
    currentMinCt = 0
    for c in childData:
        if sortByFn(c): #only check if neighbor if child is in desired data subset
            ansInCommon = countAnsInCommon(c, child)
            addIfNeighbor(c, ansInCommon, child, k, neighbors, currentMinChild, currentMinCt)
    #return classification of child
    return majorityVote(neighbors, child)
childA = [1, 0, 1, 0, 0]
childB = [0, 0, 0, 0, 0]
childC = [1, 1, 1, 1, 1]
childD = [0, 1, 0, 0, 1]
childE = [1, 0, 1, 1, 0]
childF = [0, 1, 1, 1, 1]

neighbors = [ (countAnsInCommon(childA,childD), childA), (countAnsInCommon(childB,childD), childB),
(countAnsInCommon(childE,childD), childE)]
addIfNeighbor(childF, countAnsInCommon(childF, childD), childD, 3, neighbors, childE, countAnsInCommon(childE,childD))
print neighbors
