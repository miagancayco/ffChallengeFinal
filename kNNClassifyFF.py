import csv
#given training set data and background data, combine into single list of
#data on all children
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

def addIfNeighbor(possibleNeighbor, ansInCommon, childToClassify, k, neighbors, minNeighbor):
    minCt = minNeighbor[0]
    minChild = minNeighbor[1]
    #in case where current number of neighbors is not k, do not need to check and
    #see if need to add new neighbor and remove old neighbor
    if len(neighbors) < k:
        neighbors.append((ansInCommon,possibleNeighbor))
    elif ansInCommon > minCt: #otherwise check if number of answers neighbor has in common is greater than current min
        neighbors.append((ansInCommon, possibleNeighbor))
        minNeighbor = resetMin(neighbors)
        neighbors.remove(minNeighbor)
    return

#walk down list of k neighbors, find new min child, and reset pointer
def resetMin(neighbors):
    result = neighbors[0]
    minCt = result[0]
    for n in neighbors:
        if n[0] < minCt:
            result = n
    return result

#return number of answers have in common
def countAnsInCommon(sortByFn, sortParam, childA, childB):
    notAsked = '-5' #value indicates that person was not asked given question
    skipped = '-6' # value indicates that interviewer skipped question
    notInWave = '-9' #indicates question was not asked in wave
    #iterating through all answers in child data and counting all answers have in common
    commonAns = 0
    for question in childA:
        if sortByFn(question, sortParam) and question != notAsked and question != skipped and question != notInWave and question != 'NA' and childB[question] == childA[question]:
            commonAns += 1
    return commonAns

#given a child questionnaire question-answer data pair (e.g. {m1intmon: 3}),
#return true if answer belongs to specified year
def sortByWaveNumber(question, wave):
    result = False
    questionChars = list(question)
    for char in questionChars: #according to question code, first integer will be year number
        if ord(char) == ord(wave): #check if char is a wave number (1-5)
            result = True
            break
    return result
def majorityVote(neighbors, child):
    grit, gritTotal, gpa, gpaTotal, materialHardship, mHTotal, eviction, eviction0, eviction1, layoff, layoff0, layoff1, jobTraining, jobTraining0, jobTraining1 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    #count votes for each binary variables
    #accumulate totals for continuous variables so can take average
    for n in neighbors:
        nData = n[1]
        if nData['grit'] != 'NA':
            grit += float(nData['grit'])
            gritTotal +=1
        if nData['gpa'] != 'NA':
            gpa += float(nData['gpa'])
            gpaTotal +=1
        if nData['materialHardship'] != 'NA':
            materialHardship += float(nData['materialHardship'])
            mHTotal +=1
        if nData['eviction'] != 'NA':
            if nData['eviction'] == '0':
                eviction0 += 1
            else:
                eviction1 += 1
        if nData['layoff'] != 'NA':
            if nData['layoff'] == '0':
                layoff0 += 1
            else:
                layoff1 += 1
        if nData['jobTraining'] != 'NA':
            if nData['jobTraining'] == '0':
                jobTraining0 += 1
            else:
                jobTraining1 += 1

    eviction = 0 if eviction0 > eviction1 else 1
    layoff = 0 if layoff0 > layoff1 else 1
    jobTraining = 0 if jobTraining0 > jobTraining1 else 1
    #get the average for continuous variables
    grit = grit/ gritTotal
    gpa = gpa/gpaTotal
    materialHardship = materialHardship/mHTotal
    result = {'grit': grit, 'gpa': gpa, 'materialHardship' : materialHardship, 'eviction' : eviction, 'layoff' : layoff, 'jobTraining' : jobTraining}
    return result

#given list of data on all children, parse through data, select subset according
#to sorting function; run kNN on subset in order to classify given child
def kNNClassifySubsection(sortByFn, sortParam, childToClassify, childData, k ):
    neighbors = []
    minNeighbor = (0,None)
    for child in childData:
        ansInCommon = countAnsInCommon(sortByFn, sortParam, child, childToClassify)
        addIfNeighbor(child, ansInCommon, childToClassify, k, neighbors, minNeighbor)
    return majorityVote(neighbors, child)

#childA = {'hv3m20_': 'NA', 'f4c2c': '1', 'm4m2': '1', 'f4f5':'-3'}
#childB = {'hv3m20_': 'NA', 'f4c2c': '3', 'm4m2': '1', 'f4f5':'-6'}
#childC = {'hv3m20_': 'NA', 'f4c2c': '2', 'm4m2': '0', 'f4f5':'1'}
#childD = {'hv3m20_': 'NA', 'f4c2c': '4', 'm4m2': '1', 'f4f5':'-3'}
#childE = {'hv3m20_': 'NA', 'f4c2c': '2', 'm4m2': '1', 'f4f5':'-5'}
#childF = {'hv3m20_': 'NA', 'f4c2c': '6', 'm4m2': '3', 'f4f5':'-9'}
#childData = [childB, childC, childD, childE, childF]
familyData = parseData()
first49 = []
for i in range(49):
    first49.append((0,familyData[i]))
childToClassify = familyData[49]
print majorityVote(first49, childToClassify)
