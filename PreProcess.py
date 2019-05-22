import pandas as pd
import correlation

# from BadParticipantsRemove import *
# import BadParticipantsRemove

# csv path
csvPath=''
# DataFrame for each table
FacesPictures=[]
Pictures=[]
Words=[]
NotRegUsers=[]
Report=[]
ReportPANAS=[]
UserAnswer=[]
UserTest=[]
# Answers split by question type
UserFacesAnswer=[]
UserPictureAnswer=[]
UserWordsAnswer=[]

TestsWithScores = pd.DataFrame()


# read all six tables to dataFrames
def ReadFilesToDataFrame():
    global FacesPictures,Pictures, NotRegUsers,Report,UserAnswer,UserTest, Words,ReportPANAS
    FacesPictures = pd.read_csv(csvPath + "\\FacesPictures.csv")
    # change from : "no face" to "nonFace" in FacesPictures
    FacesPictures.loc[FacesPictures['Description'] == 'no face', 'Description'] = 'nonFace'

    Pictures = pd.read_csv(csvPath + "\\Pictures.csv")
    # change from : "non" to "nothing" in Pictures
    Pictures['description'] = Pictures['description'].fillna('nothing')

    NotRegUsers = pd.read_csv(csvPath + "\\NotRegUsers.csv")
    Report = pd.read_csv(csvPath + "\\Report.csv")
    UserAnswer = pd.read_csv(csvPath + "\\UserAnswer.csv")
    UserTest = pd.read_csv(csvPath + "\\UserTest.csv")
    Words = pd.read_csv(csvPath + "\\Words.csv")
    ReportPANAS = pd.read_csv(csvPath + "\\ReportPANAS.csv")


# split user answers to 2 data frames
def SplitToPictureAndFacesAnswers():
    global UserPictureAnswer,UserFacesAnswer, UserWordsAnswer
    # get all pictures
    UserPictureAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "pic"]
    # get all faces
    UserFacesAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "face"]
    # get all words
    UserWordsAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "word"]


# add 0 or 1 if answer is right or wrong add column to UserFacesAnswer
def CheckFacesAnswers():
    global TestsWithScores
    TestsWithScores.DataFrame.to_csv(index=False)
    global UserFacesAnswer
    ranks=[]
    for index, row in UserFacesAnswer.iterrows():
        faceId=row["qId"]
        correctAnswer=getFaceCorrectAnswer(faceId)
        userAnser=row.answer
        if userAnser==correctAnswer:
            ranks.append(1)
        else:
            ranks.append(0)
    # add column of rank - 0 wrong, 1 right
    UserFacesAnswer['answerRank'] = ranks

# add rank to user answer (by coorelation)
def CheckPicturseAnswers():
    global UserPictureAnswer
    ranks = []
    # for each row in answers - calculate rank
    for index, row in UserPictureAnswer.iterrows():
        picId = row["qId"]
        correctAnswer = getPictureCorrectAnswer(picId)
        userAnser = row.answer
        rank=GetCorrelation(userAnser,correctAnswer)
        ranks.append(rank)
    # add column of rank
    UserPictureAnswer['answerRank'] = ranks

# given 2 words, gives correlation rank (between 0 and 1)
def GetCorrelation(userAnser, correctAnswer):
    return correlation.calculate_correlation(userAnser, correctAnswer)

# given faceId returns correct answer
def getFaceCorrectAnswer(faceId):
    global FacesPictures, UserAnswer
    row=FacesPictures.loc[FacesPictures['PicID'] == faceId]
    return row["Description"].values[0]

# given picId returns correct answer
def getPictureCorrectAnswer(picId):
    global Pictures
    row=Pictures.loc[Pictures['picId'] == picId]
    return row["description"].values[0]

# given wordId returns correct answer
def getWordCorrectAnswer(qId):
    global Words
    row = Words.loc[Words['wordId'] == qId]
    return row["description"].values[0]


def GetTestRates():
    global UserAnswer, TestsWithScores
    falseNegatives=pd.DataFrame(columns=['FN', 'picFN', 'wordFN', 'faceFN'])
    falsePositives=pd.DataFrame(columns=['FP', 'picFP', 'wordFP', 'faceFP'])
    trueNegatives=pd.DataFrame(columns=['TN', 'picTN', 'wordTN', 'faceTN'])
    truePositives=pd.DataFrame(columns=['TP', 'picTP', 'wordTP', 'faceTP'])
    for i in UserTest["testId"]:
        print(i)
        currAnswers=(UserAnswer.loc[UserAnswer['testId'] == i]).copy()
        currAnswers=AddRealAnswer(currAnswers)
        falseNegatives=pd.concat([falseNegatives,CalcFalseNegative(currAnswers) ],  ignore_index=True)
        falsePositives=pd.concat([falsePositives,CalcFalsePositive(currAnswers)], ignore_index=True)
        trueNegatives=pd.concat([trueNegatives,(CalcTrueNegative(currAnswers))],  ignore_index=True)
        truePositives=pd.concat([truePositives,(CalcTruePositive(currAnswers))],  ignore_index=True)
    TestsWithScores["testId"]=UserTest["testId"]
    TestsWithScores=pd.concat([TestsWithScores, falseNegatives], axis=1)
    TestsWithScores=pd.concat([TestsWithScores, falsePositives], axis=1)
    TestsWithScores=pd.concat([TestsWithScores, trueNegatives], axis=1)
    TestsWithScores=pd.concat([TestsWithScores, truePositives], axis=1)


def AddRealAnswer(currAnswers):
    realAnswer = []
    # for each row in answers - calculate rank
    for index, row in currAnswers.iterrows():
        qId = row["qId"]
        type=row["Qtype"]
        ans=""
        if(type=="pic"):
            ans = getPictureCorrectAnswer(qId)
        if (type == "word"):
            ans = getWordCorrectAnswer(qId)
        if (type == "face"):
            ans = getFaceCorrectAnswer(qId)
        realAnswer.append(ans)
    # add column of rank
    currAnswers['realAnswer'] = realAnswer
    return currAnswers

# TODO: if not answered nothing - check correlation (wrote nothing not correctly)
def CalcFalsePositive(currAnswers):
    count=0
    sum=0
    picCount=0
    picSum=0
    wordCount = 0
    wordSum = 0
    faceCount = 0
    faceSum = 0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]=="nothing" and row["answer"]!="nothing"):
                picSum=picSum+1
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "no word" and row["answer"] == "word"):
                wordSum = wordSum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "nonFace" and row["answer"] == "face"):
                faceSum = faceSum + 1
        # count only not real questions
        if(row["realAnswer"]=="nothing"):
            picCount=picCount+1
        if( row["realAnswer"] == "nonFace" ):
            faceCount=faceCount+1
        if(row["realAnswer"] == "no word"):
            wordCount=wordCount+1
    sum=picSum+faceSum+wordSum
    count=picCount+faceCount+wordCount
    return pd.DataFrame(data=[[sum/count, picSum/picCount, wordSum/wordCount, faceSum/faceCount]], columns=['FP', 'picFP', 'wordFP', 'faceFP'])

# answered "nothing" when was real
def CalcFalseNegative(currAnswers):
    count = 0
    sum = 0
    picCount = 0
    picSum = 0
    wordCount = 0
    wordSum = 0
    faceCount = 0
    faceSum = 0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]!="nothing" and row["answer"]=="nothing"):
                picSum=picSum+1
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "word" and row["answer"] == "no word"):
                wordSum = wordSum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "face" and row["answer"] == "nonFace"):
                faceSum = faceSum + 1
        # count only not real questions
        if (row["realAnswer"] != "nothing"):
            picCount = picCount + 1
        if (row["realAnswer"] != "nonFace"):
            faceCount = faceCount + 1
        if (row["realAnswer"] != "no word"):
            wordCount = wordCount + 1
    count = picCount + faceCount + wordCount
    sum = picSum + faceSum + wordSum
    return pd.DataFrame(data=[[sum / count, picSum / picCount, wordSum / wordCount, faceSum / faceCount]],columns=['FN', 'picFN', 'wordFN', 'faceFN'])

# answered "nohing" when was "nothing"
def CalcTrueNegative(currAnswers):
    count = 0
    sum = 0
    picCount = 0
    picSum = 0
    wordCount = 0
    wordSum = 0
    faceCount = 0
    faceSum = 0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]=="nothing" and row["answer"]=="nothing"):
                picSum=picSum+1
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "no word" and row["answer"] == "no word"):
                wordSum = wordSum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "nonFace" and row["answer"] == "nonFace"):
                faceSum = faceSum + 1
        # count only not real questions
        if (row["realAnswer"] == "nothing"):
            picCount = picCount + 1
        if (row["realAnswer"] == "nonFace"):
            faceCount = faceCount + 1
        if (row["realAnswer"] == "no word"):
            wordCount = wordCount + 1
    count = picCount + faceCount + wordCount
    sum = picSum + faceSum + wordSum
    return pd.DataFrame(data=[[sum / count, picSum / picCount, wordSum / wordCount, faceSum / faceCount]],
                        columns=['TN', 'picTN', 'wordTN', 'faceTN'])


# answered real when was real
def CalcTruePositive(currAnswers):
    count = 0
    sum = 0
    picCount = 0
    picSum = 0
    wordCount = 0
    wordSum = 0
    faceCount = 0
    faceSum = 0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]!="nothing" and row["answer"]!="nothing"):
                picSum=picSum+correlation.calculate_correlation(row["answer"], row["realAnswer"])
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "word" and row["answer"] == "word"):
                wordSum = wordSum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "face" and row["answer"] == "face"):
                faceSum = faceSum + 1
        # count only not real questions
        if (row["realAnswer"] != "nothing"):
            picCount = picCount + 1
        if (row["realAnswer"] != "nonFace"):
            faceCount = faceCount + 1
        if (row["realAnswer"] != "no word"):
            wordCount = wordCount + 1
    count = picCount + faceCount + wordCount
    sum = picSum + faceSum + wordSum
    return pd.DataFrame(data=[[sum / count, picSum / picCount, wordSum / wordCount, faceSum / faceCount]],
                        columns=['TP', 'picTP', 'wordTP', 'faceTP'])

def GetTestMovie():
    global TestsWithScores, UserTest, NotRegUsers, csvPath
    TestsWithScores=pd.read_csv(csvPath + '\\TestsWithScores.csv')
    TestsWithScores["video"] = ""
    for id in NotRegUsers["userID"]:
        currUserTests=(UserTest.loc[UserTest['userId'] == id]).copy()
        if(len(currUserTests)!=3):
            continue
        # sort by testId
        currUserTests.sort_values(by=['testId'])
        # add movie
        testId1 = currUserTests.iloc[[0]]["testId"].values[0]
        testId2 =currUserTests.iloc[[1]]["testId"].values[0]
        testId3 = currUserTests.iloc[[2]]["testId"].values[0]
        # calm, stress1, stress2
        if(id%2==0):
            TestsWithScores.loc[TestsWithScores['testId'] == testId1,'video']="calm"
            TestsWithScores.loc[TestsWithScores['testId'] == testId2,'video']="stress1"
            TestsWithScores.loc[TestsWithScores['testId'] == testId3,'video']="stress2"
        # stress1, stress2, calm
        else:
            TestsWithScores.loc[TestsWithScores['testId'] == testId1, 'video']= "stress1"
            TestsWithScores.loc[TestsWithScores['testId'] == testId2,'video'] = "stress2"
            TestsWithScores.loc[TestsWithScores['testId'] == testId3,'video'] = "calm"

        # add reportChange
        currUserReport = (Report.loc[Report['userId'] == id]).copy()
        # sort by report id
        currUserReport.sort_values(by=['reportId'])
        report1 = currUserReport.iloc[[0]]
        report2 = currUserReport.iloc[[1]]
        report3 = currUserReport.iloc[[2]]
        report4 = currUserReport.iloc[[3]]
        difCalm1=report2["calmLevel"].values[0]-report1["calmLevel"].values[0]
        difHappy1 = report2["happyLevel"].values[0]-report1["happyLevel"].values[0]
        difCalm2 = report3["calmLevel"].values[0]-report2["calmLevel"].values[0]
        difHappy2 =  report3["happyLevel"].values[0]-report2["happyLevel"].values[0]
        difCalm3 =  report4["calmLevel"].values[0]-report3["calmLevel"].values[0]
        difHappy3 = report4["happyLevel"].values[0]-report3["happyLevel"].values[0]
        TestsWithScores.loc[TestsWithScores['testId'] == testId1,"diffCalm"]= difCalm1
        TestsWithScores.loc[TestsWithScores['testId'] == testId2,"diffCalm"]= difCalm2
        TestsWithScores.loc[TestsWithScores['testId'] == testId3,"diffCalm"]= difCalm3
        TestsWithScores.loc[TestsWithScores['testId'] == testId1,"diffHappy"]= difHappy1
        TestsWithScores.loc[TestsWithScores['testId'] == testId2,"diffHappy"]= difHappy2
        TestsWithScores.loc[TestsWithScores['testId'] == testId3,"diffHappy"]= difHappy3
        # add happy and calm report
        TestsWithScores.loc[TestsWithScores['testId'] == testId1,"CalmLevel"]= report2["calmLevel"].values[0]
        TestsWithScores.loc[TestsWithScores['testId'] == testId2,"CalmLevel"]= report3["calmLevel"].values[0]
        TestsWithScores.loc[TestsWithScores['testId'] == testId3,"CalmLevel"]= report4["calmLevel"].values[0]

        TestsWithScores.loc[TestsWithScores['testId'] == testId1,"PositiveLevel"]= report2["happyLevel"].values[0]
        TestsWithScores.loc[TestsWithScores['testId'] == testId2,"PositiveLevel"]= report3["happyLevel"].values[0]
        TestsWithScores.loc[TestsWithScores['testId'] == testId3,"PositiveLevel"]= report4["happyLevel"].values[0]


def SaveTests():
    global TestsWithScores, csvPath
    TestsWithScores.to_csv(csvPath + '\\TestsWithScores.csv', encoding='utf-8', index=False)

def LoadTestsWithScores():
    global TestsWithScores
    TestsWithScores = pd.read_csv(csvPath + "\\TestsWithScores.csv")

def addUserInfoToTest():
    global TestsWithScores, NotRegUsers, UserTest
    testsCopy=TestsWithScores.copy()
    TestsWithScores['userId'] = ''
    TestsWithScores['age'] = ''
    TestsWithScores['gender'] = ''
    TestsWithScores['englishLevel'] = ''
    TestsWithScores['hand'] = ''
    for index, row in testsCopy.iterrows():
        temp = (UserTest.loc[UserTest['testId'] == row['testId']]).copy()
        id=temp['userId'].iloc[0]
        currentUser = (NotRegUsers.loc[NotRegUsers['userID'] == id]).copy()
        TestsWithScores.loc[TestsWithScores['testId']==row['testId'],'userId'] = currentUser['userID'].iloc[0]
        TestsWithScores.loc[TestsWithScores['testId']==row['testId'],'age'] = currentUser['age'].iloc[0]
        TestsWithScores.loc[TestsWithScores['testId']==row['testId'],'gender'] = currentUser['gender'].iloc[0]
        TestsWithScores.loc[TestsWithScores['testId']==row['testId'],'englishLevel'] = currentUser['email'].iloc[0]
        TestsWithScores.loc[TestsWithScores['testId']==row['testId'],'hand'] = currentUser['hand'].iloc[0]