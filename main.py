import PreProcess
import BadParticipantsRemove

def main(dataPath):
    PreProcess.csvPath=dataPath
    PreProcess.ReadFilesToDataFrame()
    PreProcess.SplitToPictureAndFacesAnswers()
    PreProcess.CheckPicturseAnswers()
    BadParticipantsRemove.RemoveUnwantedParticipant()
    PreProcess.CheckFacesAnswers()

main('C:\\Users\\nogahm\\PycharmProjects\\P-Sense-Data-Analysis\\tables')