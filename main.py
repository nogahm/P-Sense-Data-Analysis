import PreProcess
import BadParticipantsRemove
import Graphs

def main(dataPath):
    PreProcess.csvPath=dataPath
    PreProcess.ReadFilesToDataFrame()
    PreProcess.SplitToPictureAndFacesAnswers()
    # BadParticipantsRemove.RemoveParticipantsNotReportPANAS()
    # BadParticipantsRemove.RemoveParticipantNotFinish()
    # BadParticipantsRemove.RemoveUnwantedParticipant()
    # PreProcess.CheckPicturseAnswers()
    # PreProcess.LoadTestsWithScores()
    # PreProcess.GetTestRates()
    # PreProcess.GetTestMovie()
    # PreProcess.GetTestChangeInEmotion()
    # PreProcess.CheckFacesAnswers()
    # PreProcess.addUserInfoToTest()
    # PreProcess.SaveTests()
    PreProcess.LoadTestsWithScores()
    # Graphs.ShowFalsePositiveGraphs(PreProcess.TestsWithScores.loc[PreProcess.TestsWithScores['video']=='stress2'])
    Graphs.ShowDifferenceBetweenTests(PreProcess.TestsWithScores)

main('tables')

