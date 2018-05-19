import csv
import math
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
<<<<<<< HEAD

=======
>>>>>>> eaf42fad668a8f0e434cc82a7cfd79a5cde3610f
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
<<<<<<< HEAD
    interviewee = question[0]
    waveNum = question[1]
    sectionNum = question[2]
    if interviewee == 'm' or interviewee == 'f': #check if was answered by parent
    #check wave number and section letter - education questions only asked in waves 2, 3, and 4 in section k and waves 1 and 5 in section i in questionnaires
        if waveNum == '2' or waveNum == '3' or waveNum == '4':
            if sectionNum == 'k':
                result = True
        elif waveNum == '5':
            if sectionNum == 'i':
                result = True
    return result
#returns true if question pertains to income status of family
def isFamilyIncomeQuestion(question):
    result = False
    interviewee = question[0]
    waveNum = question[1]
    sectionNum = question[2]
    if interviewee == 'm' or interviewee == 'f': #check if was answered by parent
    #check wave and section number - family income questions only asked in section l for waves 2 3 and 4 and section j in wave 5
        if waveNum == '2' or waveNum == '3' or waveNum == '4':
            if sectionNum == 'l':
                result = True
        elif waveNum == '5' or waveNum == '1':
            if sectionNum == 'j':
                result = True
    return result
#returns true if question pertains to relationships within family
def isFamilyRelationshipQuestion(question):
    result = False
    interviewee = question[0]
    waveNum = question[1]
    sectionNum = question[2]
    if interviewee == 'm' or interviewee == 'f': #check if was answered by parent
    #check wave and section number - family relationship questions only asked in sections a-d for all waves
        if waveNum == '1' or waveNum == '2' or waveNum == '3' or waveNum == '4' or waveNum == '5':
            if sectionNum == 'a' or sectionNum == 'b' or sectionNum == 'c' or sectionNum == 'd':
                result = True
    return result
#returns true if question pertains to living environment
def isLivingEnvironmentQuestion(question):
    result = False
    interviewee = question[0]
    waveNum = question[1]
    sectionNum = question[2]
    if interviewee == 'm' or interviewee == 'f': #check if was answered by parent
    #check wave and section number - living environment questions in wave 1 section f, wave 2 section h, waves 3 and 4 section i, and wave 5 section f
        if waveNum == '1':
            if sectionNum == 'f':
                result = True
        if waveNum == '2':
            if sectionNum == 'h':
                result = True
        if waveNum == '3' or waveNum == '4':
            if sectionNum == 'i':
                result = True
        if waveNum == '5':
            if sectionNum == 'f':
                result = True
    return result
#returns true if question pertains to religion of family
def isFamilyReligionQuestion(question):
    result = False
    interviewee = question[0]
    waveNum = question[1]
    sectionNum = question[2]
    if interviewee == 'm' or interviewee == 'f': #check if was answered by parent
    #check wave and section number - family religion questions asked in waves 3 and 4 and section r and wave 5 section h
        if waveNum == '3' or waveNum == '4':
            if sectionNum == 'r':
                result = True
        if waveNum == '5':
            if sectionNum == 'h':
                result = True
    return result
=======
    if question[0] == 'm' or question[0] == 'f': #check if was answered by parent
    #check wave and section number - education questions only asked in section k for waves 2 and 4 and section i in wave 5
        if question[1] == '2' or question[1] == '4':
            if question[2] == 'k':
                result = True
        elif question[1] == '5' and question[2] == 'i':
            result = True
    return result

>>>>>>> eaf42fad668a8f0e434cc82a7cfd79a5cde3610f
#given list of data on all children, parse through data, select subset according
#to sorting function; run kNN on subset in order to classify given child
def kNNClassify(childToClassify, childData, k, sortByFn=None):
    for child in childData: # iterate through data and count answers have in common with child to classify
        ansInCommon = countSortedAnsInCommon(child, childToClassify, sortByFn) if sortByFn != None else countAnsInCommon(child, childToClassify)
        child['ansInCommon'] = ansInCommon
    neighbors = getKNeighbors(childData, k)
    return majorityVote(neighbors, childToClassify)
<<<<<<< HEAD

#Given a (preferably blank) csv file, runs kNN Classification on test data
#To select for only certain questions to be considered in kNN classification, you
#may pass in a sorting functon (see above sorting methods for examples )
def recordResults(fileName, sortFn=None):
    with open(fileName, 'w') as csvfile:
=======
def recordResults():
    with open('resultskNNClassifyEducationalFactors.csv', 'w') as csvfile:
>>>>>>> eaf42fad668a8f0e434cc82a7cfd79a5cde3610f
        fieldnames = ['challengeID', 'gpa', 'grit', 'materialHardship', 'eviction', 'layoff', 'jobTraining']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        familyData = parseData()
        trainSet = familyData[0]
        testSet = familyData[1]
        for child in testSet:
<<<<<<< HEAD
            prediction = kNNClassify(child, trainSet, 11, sortFn)
=======
            print child['challengeID']
            prediction = kNNClassify(child, trainSet, 11, isParentEducationQuestion)
            print prediction
>>>>>>> eaf42fad668a8f0e434cc82a7cfd79a5cde3610f
            writer.writerow({'challengeID': prediction['challengeID'], 'gpa': prediction['gpa'], 'grit': prediction['grit'], 'materialHardship': prediction['materialHardship'], 'eviction': prediction['eviction'], 'layoff': prediction['layoff'], 'jobTraining': prediction['jobTraining']})
    return
#find average difference between continuous variable scores and percentage of times
#correctly predict binary variables - answers are written onto results file
def comparePredictions(resultsFile):
    predictions = []
    testSet = []

    gritDiffAvg, gpaDiffAvg, mhDiffAvg, gritTotal, gpaTotal, mhTotal, layoffCorrectTotal,layoffTotal, evictionCorrectTotal, evictionTotal, jtCorrectTotal, jtTotal = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    with open(resultsFile) as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ',')
        for row in reader:
            predictions.append(row)
    with open('test.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ',')
        for row in reader:
            testSet.append(row)
    for p in predictions:
        pID = p['challengeID']
        for t in testSet:
            if t['challengeID'] == pID: #once found corresponding child in testData compare scores
                #get average difference in GPA, grit, and materialHardship scores
                #if score is 'NA' for either, do not add to average
                if p['gpa'] != 'NA' and t['gpa'] != 'NA':
                    gpaDiff = math.fabs(float(p['gpa']) - float(t['gpa']))
                    gpaDiffAvg += gpaDiff
                    gpaTotal +=1
                if p['grit'] != 'NA' and t['grit'] != 'NA':
                    gritDiff = math.fabs(float(p['grit']) - float(t['grit']))
                    gritDiffAvg += gritDiff
                    gritTotal +=1
                if p['materialHardship'] != 'NA' and t['materialHardship'] != 'NA':
                    mhDiff = math.fabs(float(p['materialHardship']) - float(t['materialHardship']))
                    mhDiffAvg += mhDiff
                    mhTotal +=1
                #for binary values (eviction, layoff, jobTraining), calculate percentage of correct predictions
                if p['layoff'] == t['layoff']:
                    layoffCorrectTotal += 1
                if p['eviction'] == t['eviction']:
                    evictionCorrectTotal += 1
                if p['jobTraining'] == t['jobTraining']:
                    jtCorrectTotal += 1
                break
    gpaDiffAvg = gpaDiffAvg/gpaTotal if total !=0 else -1
    gritDiffAvg = gritDiffAvg/gritTotal if total !=0 else -1
    mhDiffAvg = mhDiffAvg/mhTotal if total !=0 else -1

    return [gpaDiffAvg, gritDiffAvg, mhDiffAvg, layoffCorrectTotal, evictionCorrectTotal, jtCorrectTotal]
