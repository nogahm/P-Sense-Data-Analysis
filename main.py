import PreProcess
import BadParticipantsRemove

def main(dataPath):
    PreProcess.csvPath=dataPath
    PreProcess.ReadFilesToDataFrame()
    PreProcess.SplitToPictureAndFacesAnswers()
    # BadParticipantsRemove.RemoveParticipantNotFinish()
    # BadParticipantsRemove.RemoveUnwantedParticipant()
    # PreProcess.CheckPicturseAnswers()
    PreProcess.GetTestRates()
    PreProcess.GetTestMovie()
    PreProcess.GetTestChangeInEmotion()
    PreProcess.CheckFacesAnswers()


main('tables')

