import pandas as pd
# spacy - for semantic corelation

# csv path
csvPath=''
# DataFrame for each table
FacesPictures=[]
Pictures=[]
NotRegUsers=[]
Report=[]
UserAnswer=[]
UserTest=[]

UserFacesAnswer=[]
UserPictureAnswer=[]

# read all six tables to dataFrames
def ReadFilesToDataFrame():
    global FacesPictures,Pictures, NotRegUsers,Report,UserAnswer,UserTest
    FacesPictures = pd.read_csv(csvPath + "\\FacesPictures.csv")
    Pictures = pd.read_csv(csvPath + "\\Pictures.csv")
    NotRegUsers = pd.read_csv(csvPath + "\\NotRegUsers.csv")
    Report = pd.read_csv(csvPath + "\\Report.csv")
    UserAnswer = pd.read_csv(csvPath + "\\UserAnswer.csv")
    UserTest = pd.read_csv(csvPath + "\\UserTest.csv")

# split user answers to 2 data frames
def SplitToPictureAndFacesAnswers():
    global UserPictureAnswer,UserFacesAnswer
    # get all pictures
    UserPictureAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "pic"]
    # get all faces
    UserFacesAnswer=UserAnswer.loc[UserAnswer['Qtype'] == "face"]

# add 0 or 1 if answer is right or wrong add column to UserFacesAnswer
def CheckFacesAnswers():
    for index,row in UserFacesAnswer:
        faceId=row["qId"]
        correctAnswer=getPictureCorrectAnswer(faceId)
        userAnser=row["answer"]
        if userAnser==correctAnswer:
            row["answerRank"]=1
        else:
            row["answerRank"] = 0

# TODO - get correlation between correct answer and user answer
def CheckPicturseAnswers():
    return 0

# given faceId returns correct answer
def getPictureCorrectAnswer(faceId):
    row=FacesPictures.loc[UserAnswer['PicID'] == faceId]
    return row["Description"]

# given picId returns correct answer
def getPictureCorrectAnswer(picId):
    row=Pictures.loc[UserAnswer['picID'] == picId]
    return row["Description"]

# TODO - check if user answer wrong to one of the test question - remove participant from all tables
def RemoveUnwantedParticipant():
    pass


def main(dataPath):
    global csvPath
    csvPath=dataPath
    ReadFilesToDataFrame()
    SplitToPictureAndFacesAnswers()
    CheckPicturseAnswers()
    RemoveUnwantedParticipant()
    CheckFacesAnswers()

main('C:\\Users\\nogahm\\PycharmProjects\\P-Sense-Data-Analysis\\tables')