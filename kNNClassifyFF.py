# given training set data and background data, combine into single children list of
#lists, where each list represents each child
import csv
def parseData():
    familyData = [] # list of child lists that will return
    with open('train.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            familyData.append(row)
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



#given a dataset representing numerous families' answers to a specific questionnaire subsection
#(e.g. child health, mother father relationships, household economic status) and a
#child to classify, return classification of a child based on top k neighbors with most answers
#in common
def classifySubsection(subsection, child, k):
    neighbors = getNeighbors(subsection, child, k)
    #classify child based on top k neighbors
    majorityVote(neighbors, child)
    return

#return k neighbors that share most answers in common
def getNeighbors(subsection, childToClassify, k):
    neighbors = []
    totalNeighbors = 0
    ansInCommon = countAnsInCommon(subsection, childToClassify) #list of children and number of answers have in common with child
    maxAnsInCommon = 0
    while totalNeighbors < k:
        newNeighbor = ansInCommon[0] #need better name
        for child in ansInCommon:
            currentCt = child[1]
            if currentCt > maxAnsInCommon:
                maxAnsInCommon = currentCt
                newNeighbor = child
        #once find neighbor, add to result, and remove from ansInCommon
        #list so can find next max
        neighbors.append(newNeighbor[0])
        ansInCommon.remove(newNeighbor)
        totalNeighbors +=1
    return neighbors
#return a list of children in subsection and corresponding number of answers have
#in common
def countAnsInCommon(subsection, childToClassify):
    result = []
    #for each child represented, count answers have in common with child
    for child in subsection:
        commonAns = 0
        #iterating through all answers in child data
        for i in range(0, len(child)): #adjust so make sure that skip over parts of list that have to do with classifications
            if childToClassify[i] == child[i]:
                commonAns += 1
        childAnswers = (child, commonAns) #better name needed
        result.append(childAnswers)
    return result

data = parseData()
print data[0]
