import PreProcess

from PreProcess import *

removedUsers=[]

# check if user answered wrong to one of the test question - remove participant from all tables
def RemoveUnwantedParticipant():
    badTests=getBadTests()
    badParticipant=getBadParticipant(badTests)
    removeAllTestsOfBadParticipant(badParticipant)

# check if answered wrong in one of the constant question
def getBadTests():
    constantPictures=['25', '2', '37', '44', '23']
    badTests=[]
    # get data of question
    constansAnswers=PreProcess.UserPictureAnswer.loc[PreProcess.UserPictureAnswer['qId'].isin(constantPictures)]
    for index,row in constansAnswers.iterrows():
        correctAnswer=getPictureCorrectAnswer(row['qId'])
        userAnswer=row.answer
        # if bigger than 0.9 - assume he is right
        if(GetCorrelation(userAnswer,correctAnswer)<0.9):
            badTests.append(row.testId)
    return badTests

# given bad tests - returns the users answered it
def getBadParticipant(badTests):
    global UserTest
    badParticipant=UserTest.loc[UserTest['testId'].isin(badTests)]
    return (badParticipant.userId).toList()

# given list of users - delete all their tests from UserFacesAnswer, UserPictureAnswer, UserTest, Report
def removeAllTestsOfBadParticipant(badParticipant):
    # global UserFacesAnswer, UserPictureAnswer, UserTest, Report, removedUsers
    removedUsers=badParticipant
    # get tests to remove by bad participants
    testsToRemove=UserTest.loc[UserTest['userId'].isin(badParticipant)]
    # remove from UserFacesAnswer
    indexNames = UserFacesAnswer[(UserFacesAnswer['testId'].isin(testsToRemove))].index
    UserFacesAnswer.drop(indexNames, inplace=True)
    # remove from UserPictureAnswer
    indexNames = UserPictureAnswer[(UserPictureAnswer['testId'].isin(testsToRemove))].index
    UserPictureAnswer.drop(indexNames, inplace=True)
    # remove from UserTest
    indexNames = UserTest[(UserTest['testId'].isin(testsToRemove))].index
    UserTest.drop(indexNames, inplace=True)
    # remove from Report
    indexNames = Report[(Report['userId'].isin(badParticipant))].index
    Report.drop(indexNames, inplace=True)

def RemoveParticipantsNotReportPANAS():
    # save only tests with users who finish all experimant
    # PreProcess.UserTest = PreProcess.UserTest.join(PreProcess.ReportPANAS, left_on='userId', right_on='userId', how='left')
    PreProcess.UserTest=PreProcess.UserTest.merge(PreProcess.ReportPANAS , on='userId', how='inner')

