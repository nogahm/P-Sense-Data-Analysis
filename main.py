import PreProcess
import BadParticipantsRemove
import Graphs

def main(dataPath):
    PreProcess.csvPath=dataPath
    # PreProcess.ReadFilesToDataFrame()
    # PreProcess.SplitToPictureAndFacesAnswers()
    # BadParticipantsRemove.RemoveParticipantsNotReportPANAS()
    # PreProcess.GetTestRates()
    # PreProcess.SaveTests()
    # PreProcess.LoadTestsWithScores()

    # PreProcess.GetTestMovie()
    # PreProcess.addUserInfoToTest()
    # PreProcess.SaveTests()
    # PreProcess.LoadTestsWithScores()
    PreProcess.LoadTestsWithScores()

    Graphs.ShowFalsePositiveGraphs(PreProcess.TestsWithScores.loc[PreProcess.TestsWithScores['video']=='calm'])
    # Graphs.ShowDifferenceBetweenTests(PreProcess.TestsWithScores)

    # firstCalm=PreProcess.TestsWithScores.loc[PreProcess.TestsWithScores['userId']==1]
    Graphs.GraphByQuestionType(PreProcess.TestsWithScores)

    Graphs.CalmMinusPositiveGraph(PreProcess.TestsWithScores)
    # Graphs.DiffCalmGraph(PreProcess.TestsWithScores)

main('tables')

