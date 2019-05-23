import PreProcess
import BadParticipantsRemove
import Graphs

def main(dataPath):
    #PreProcess.csvPath=dataPath
    #PreProcess.ReadFilesToDataFrame()
    #PreProcess.SplitToPictureAndFacesAnswers()
    #BadParticipantsRemove.RemoveParticipantsNotReportPANAS()
    #PreProcess.GetTestRates()
    #PreProcess.SaveTests()
    #PreProcess.LoadTestsWithScores()

    #PreProcess.GetTestMovie()
    #PreProcess.addUserInfoToTest()
    ## PreProcess.SaveTests()
   # PreProcess.LoadTestsWithScores()
    # Graphs.ShowFalsePositiveGraphs(PreProcess.TestsWithScores.loc[PreProcess.TestsWithScores['video']=='calm'])
    # Graphs.ShowDifferenceBetweenTests(PreProcess.TestsWithScores)
    Graphs.GraphByQuestionType(PreProcess.TestsWithScores)

main('tables')

