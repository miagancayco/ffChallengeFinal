# given training set data and background data, combine into single children list of
#lists, where each list represents each child
import csv
def parseData():
    familyData = [] # list of child lists that will return
    with open('train.csv') as csvfile:
        tReader = csv.reader(csvfile, delimiter = ",")
        for trainInfo in tReader:
            familyData.append(trainInfo)
    with open('background.csv') as csvfile:
        bReader = csv.reader(csvfile, delimiter = ",")
        for famInfo in bReader:
            famID = famInfo[0]
            for family in familyData:
                familyID = family[0]
                #add corresponding background information to appropriate family
                #in familyData by checking ID number
                if(famID == familyID):
                    family.extend(famInfo)
    return familyData
classifySubsection(subsection, child, k){

}
parseData()
