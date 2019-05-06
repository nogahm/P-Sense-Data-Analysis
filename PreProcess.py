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
    global FacesPictures,Pictures, NotRegUsers,Report,UserAnswer,UserTest, Words
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
    falseNegatives=[]
    falsePositives=[]
    trueNegatives=[]
    truePositives=[]
    for i in UserTest["testId"]:
        print(i)
        currAnswers=(UserAnswer.loc[UserAnswer['testId'] == i]).copy()
        currAnswers=AddRealAnswer(currAnswers)
        falseNegatives.append(CalcFalseNegative(currAnswers))
        falsePositives.append(CalcFalsePositive(currAnswers))
        trueNegatives.append(CalcTrueNegative(currAnswers))
        truePositives.append(CalcTruePositive(currAnswers))
    TestsWithScores["testId"]=UserTest["testId"]
    TestsWithScores["falseNegative"] = falseNegatives
    TestsWithScores["falsePositive"] = falsePositives
    TestsWithScores["trueNegative"] = trueNegatives
    TestsWithScores["truePositive"] = truePositives


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

# TODO: if not answered nothing - check correlation
def CalcFalsePositive(currAnswers):
    count=0
    sum=0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]=="nothing" and row["answer"]!="nothing"):
                sum=sum+1
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "no word" and row["answer"] == "word"):
                sum = sum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "nonFace" and row["answer"] == "face"):
                sum = sum + 1
        count=count+1
    return sum/count

# answered "nothing" when was real
def CalcFalseNegative(currAnswers):
    count=0
    sum=0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]!="nothing" and row["answer"]=="nothing"):
                sum=sum+1
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "word" and row["answer"] == "no word"):
                sum = sum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "face" and row["answer"] == "nonFace"):
                sum = sum + 1
        count=count+1
    return sum/count


def CalcTrueNegative(currAnswers):
    count=0
    sum=0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]=="nothing" and row["answer"]=="nothing"):
                sum=sum+1
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "no word" and row["answer"] == "no word"):
                sum = sum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "nonFace" and row["answer"] == "nonFace"):
                sum = sum + 1
        count=count+1
    return sum/count

# TODO: check with hilla
def CalcTruePositive(currAnswers):
    count=0
    sum=0
    for index, row in currAnswers.iterrows():
        if(row["Qtype"]=="pic"):
            if(row["realAnswer"]!="nothing" and row["answer"]!="nothing"):
                sum=sum+correlation.calculate_correlation(row["answer"], row["realAnswer"])
        if (row["Qtype"] == "word"):
            if (row["realAnswer"] == "word" and row["answer"] == "word"):
                sum = sum + 1
        if (row["Qtype"] == "face"):
            if (row["realAnswer"] == "face" and row["answer"] == "face"):
                sum = sum + 1
        count=count+1
    return sum/count


def GetTestMovie():
    global TestsWithScores, UserTest, NotRegUsers
    for id in NotRegUsers["userID"]:
        currUserTests=(UserTest.loc[UserTest['userId'] == id]).copy()
        # sort by testId
        currUserTests.sort_values(by=['testId'])
        # add movie
        testId1 = currUserTests["testId"][0]
        testId2 = currUserTests["testId"][1]
        testId3 = currUserTests["testId"][2]
        # calm, stress1, stress2
        if(id%2==0):
            TestsWithScores["video"][testId1]="calm"
            TestsWithScores["video"][testId2]="stress1"
            TestsWithScores["video"][testId3]="stress2"
        # stress1, stress2, calm
        else:
            TestsWithScores["video"][testId1] = "stress1"
            TestsWithScores["video"][testId2] = "stress2"
            TestsWithScores["video"][testId3] = "calm"

        # add reportChange
        currUserReport = (Report.loc[UserTest['userId'] == id]).copy()
        # sort by report id
        currUserReport.sort_values(by=['reportId'])
        report1 = currUserReport[0]
        report2 = currUserReport[1]
        report3 = currUserReport[2]
        report4 = currUserReport[3]
        difCalm1=report1["calmLevel"]-report2["calmLevel"]
        difHappy1 = report1["happyLevel"] - report2["happyLevel"]
        difCalm2 = report2["calmLevel"] - report3["calmLevel"]
        difHappy2 = report2["happyLevel"] - report3["happyLevel"]
        difCalm3 = report3["calmLevel"] - report4["calmLevel"]
        difHappy3 = report3["happyLevel"] - report4["happyLevel"]
        TestsWithScores["diffCalm"][testId1] = difCalm1
        TestsWithScores["diffCalm"][testId2] = difCalm2
        TestsWithScores["diffCalm"][testId3] = difCalm3
        TestsWithScores["diffHappy"][testId1] = difHappy1
        TestsWithScores["diffHappy"][testId2] = difHappy2
        TestsWithScores["diffHappy"][testId3] = difHappy3
