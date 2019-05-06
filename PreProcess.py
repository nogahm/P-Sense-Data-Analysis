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


UserFacesAnswer=[]
UserPictureAnswer=[]

# read all six tables to dataFrames
def ReadFilesToDataFrame():
    global FacesPictures,Pictures, NotRegUsers,Report,UserAnswer,UserTest
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
    global UserPictureAnswer,UserFacesAnswer
    # get all pictures
    UserPictureAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "pic"]
    # get all faces
    UserFacesAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "face"]

# add 0 or 1 if answer is right or wrong add column to UserFacesAnswer
def CheckFacesAnswers():
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


