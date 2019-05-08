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
    # PreProcess.GetTestRates()
    # PreProcess.SaveTests()
    PreProcess.GetTestMovie()
    Graphs.ShowFalsePositiveGraphs()
    # PreProcess.GetTestChangeInEmotion()
    # PreProcess.CheckFacesAnswers()


main('tables')

