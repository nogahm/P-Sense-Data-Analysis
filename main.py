import PreProcess
import BadParticipantsRemove

def main(dataPath):
    PreProcess.csvPath=dataPath
    PreProcess.ReadFilesToDataFrame()
    PreProcess.SplitToPictureAndFacesAnswers()
    BadParticipantsRemove.RemoveUnwantedParticipant()
    PreProcess.CheckPicturseAnswers()
    PreProcess.CheckFacesAnswers()

main('tables')