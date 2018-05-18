import csv
#given training set data and background data, combine into single list of
#data on all children
def parseData():
    trainSet = []
    testSet = []
    familyData = (trainSet,testSet) # list of child lists that will return
    with open('train.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            trainSet.append(row)
    with open('test.csv') as csvfile:
        tReader = csv.DictReader(csvfile)
        for row in tReader:
            testSet.append(row)
    with open('background.csv') as csvfile: #ugh this code is so ugly
        bReader = csv.DictReader(csvfile)
        for row in bReader:
            famID = float(row.get('challengeID'))
            #separate test and training sets
            for family in trainSet:
                trainFamID = float(family.get('challengeID'))
                #add corresponding background information to appropriate family
                #in familyData by checking ID number
                if trainFamID > famID:
                    break
                if famID == trainFamID:
                    family.update(row)
            for family in testSet:
                testFamID = float(family.get('challengeID'))
                if testFamID > famID:
                    break
                if testFamID == famID:
                    family.update(row)
    return familyData
#sort data according to answers in common with child to classify and return first k
def getKNeighbors(familyData, k):
    sortedFamilyData= sorted(familyData, key = lambda k: k['ansInCommon'], reverse=True)
    kNeighbors= sortedFamilyData[0:k]
    return kNeighbors
def countAnsInCommon(childA, childB):
    notAsked = '-5' #value indicates that person was not asked given question
    skipped = '-6' # value indicates that interviewer skipped question
    notInWave = '-9' #indicates question was not asked in wave
    #iterating through all answers in child data and counting all answers have in common
    commonAns = 0
    for question in childA:
        if question in childB and question != notAsked and question != skipped and question != notInWave and question != 'NA' and childB[question] == childA[question]:
            commonAns += 1
    return commonAns
def countSortedAnsInCommon(childA, childB, sortByFn):
    notAsked = '-5' #value indicates that person was not asked given question
    skipped = '-6' # value indicates that interviewer skipped question
    notInWave = '-9' #indicates question was not asked in wave
    #iterating through all answers in child data and counting all answers have in common
    commonAns = 0
    for question in childA:
        if sortByFn(question) and question != notAsked and question != skipped and question != notInWave and question != 'NA' and childB[question] == childA[question]:
            commonAns += 1
    return commonAns
#given a child questionnaire question-answer data pair (e.g. {m1intmon: 3}),
#return true if answer belongs to specified year
def sortByWaveNumber(question, wave):
    result = False
    #deal with ffcc and kind questions from survey if wave number is not 5
    if ord(wave) != 53 and  question[0:4] == 'ffcc' or question[0:4] == 'kind':
            return result
    questionChars = list(question)
    yearNum = ''
    for char in questionChars: #according to question code, first integer will be year number
        if ord(char) > 48 and ord(char) < 54 : #check if char is a wave number (1-5)
            yearNum = char
            break
    if yearNum == wave:
        result = True
    return result
def majorityVote(neighbors, child):
    grit, gritTotal, gpa, gpaTotal, materialHardship, mHTotal, eviction, eviction0, eviction1, layoff, layoff0, layoff1, jobTraining, jobTraining0, jobTraining1 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    #count votes for each binary variables
    #accumulate totals for continuous variables so can take average
    for n in neighbors:
        if n['grit'] != 'NA':
            grit += float(n['grit'])
            gritTotal +=1
        if n['gpa'] != 'NA':
            gpa += float(n['gpa'])
            gpaTotal +=1
        if n['materialHardship'] != 'NA':
            materialHardship += float(n['materialHardship'])
            mHTotal +=1
        if n['eviction'] != 'NA':
            if n['eviction'] == '0':
                eviction0 += 1
            else:
                eviction1 += 1
        if n['layoff'] != 'NA':
            if n['layoff'] == '0':
                layoff0 += 1
            else:
                layoff1 += 1
        if n['jobTraining'] != 'NA':
            if n['jobTraining'] == '0':
                jobTraining0 += 1
            else:
                jobTraining1 += 1

    eviction = 0 if eviction0 > eviction1 else 1
    layoff = 0 if layoff0 > layoff1 else 1
    jobTraining = 0 if jobTraining0 > jobTraining1 else 1
    #get the average for continuous variables
    grit = grit/ gritTotal if gritTotal != 0 else 'NA'
    gpa = gpa/gpaTotal if gpaTotal != 0 else 'NA'
    materialHardship = materialHardship/mHTotal if mHTotal != 0 else 'NA'
    result = {'challengeID': child['challengeID'], 'grit': grit, 'gpa': gpa, 'materialHardship' : materialHardship, 'eviction' : eviction, 'layoff' : layoff, 'jobTraining' : jobTraining}
    return result
#returns true if question pertains to education and employment status of parent
def isParentEducationQuestion(question):
    result = False
    if question[0] == 'm' or question[0] == 'f': #check if was answered by parent
    #check wave and section number - education questions only asked in section k for waves 2 and 4 and section i in wave 5
        if question[1] == '2' or question[1] == '4':
            if question[2] == 'k':
                result = True
        elif question[1] == '5' and question[2] == 'i':
            result = True
    return result

#given list of data on all children, parse through data, select subset according
#to sorting function; run kNN on subset in order to classify given child
def kNNClassify(childToClassify, childData, k, sortByFn=None):
    for child in childData: # iterate through data and count answers have in common with child to classify
        ansInCommon = countSortedAnsInCommon(child, childToClassify, sortByFn) if sortByFn != None else countAnsInCommon(child, childToClassify)
        child['ansInCommon'] = ansInCommon
    neighbors = getKNeighbors(childData, k)
    return majorityVote(neighbors, childToClassify)
def recordResults():
    with open('resultskNNClassifyEducationalFactors.csv', 'w') as csvfile:
        fieldnames = ['challengeID', 'gpa', 'grit', 'materialHardship', 'eviction', 'layoff', 'jobTraining']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        familyData = parseData()
        trainSet = familyData[0]
        testSet = familyData[1]
        for child in testSet:
            print child['challengeID']
            prediction = kNNClassify(child, trainSet, 11, isParentEducationQuestion)
            print prediction
            writer.writerow({'challengeID': prediction['challengeID'], 'gpa': prediction['gpa'], 'grit': prediction['grit'], 'materialHardship': prediction['materialHardship'], 'eviction': prediction['eviction'], 'layoff': prediction['layoff'], 'jobTraining': prediction['jobTraining']})
    return
recordResults()
