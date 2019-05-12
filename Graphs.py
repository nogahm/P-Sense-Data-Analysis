import PreProcess
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")


import pandas as pd
import numpy as np

# def ShowFalsePositiveGraphs():
#     TestsWithInfo=PreProcess.TestsWithScores.copy()
#     # change diff calm for graph - bigger diff=more stress
#     TestsWithInfo['diffCalm']=TestsWithInfo['diffCalm']*(-1)
#     # for each diffCalm - average of all other columns
#     diffCalmAVG=TestsWithInfo.groupby('diffCalm').mean()
#     # FP and change in calm - Graph
#     # plt.plot(diffCalmAVG.index, diffCalmAVG['falsePositive'])
#     # plt.show()
#
#     # for each diffHappy - average of all other columns
#     # diffHappyAVG=TestsWithInfo.groupby('diffHappy').mean()
#     # plt.plot(diffHappyAVG.index, diffHappyAVG['falsePositive'])
#     # plt.show()
#     GraphForColumns('CalmLevel','falsePositive',TestsWithInfo)
#     print('1')

def ShowFalsePositiveGraphs(TestsWithInfo):
    # CalmLevel Graph
    # FP
    CalmData=TestsWithInfo.groupby('CalmLevel').mean()
    plt.plot(CalmData.index, CalmData['FP'])
    plt.plot(CalmData.index, CalmData['picFP'])
    plt.plot(CalmData.index, CalmData['wordFP'])
    plt.plot(CalmData.index, CalmData['faceFP'])
    plt.legend(['Averaged False Positive', 'Pictures False Positive', 'Words False Positive', 'Faces False Positive'], loc='upper left')
    plt.title('Calm Level - False Positive')
    plt.xlabel('Calm Level')
    plt.ylabel('False Positive')
    plt.show()

    # NegativeLevel Graph
    # FP
    CalmData = TestsWithInfo.groupby('PositiveLevel').mean()
    plt.plot(CalmData.index, CalmData['FP'])
    plt.plot(CalmData.index, CalmData['picFP'])
    plt.plot(CalmData.index, CalmData['wordFP'])
    plt.plot(CalmData.index, CalmData['faceFP'])
    plt.legend(['Averaged False Positive', 'Pictures False Positive', 'Words False Positive', 'Faces False Positive'],
               loc='upper left')
    plt.title('Positive Level - False Positive')
    plt.xlabel('Positive Level')
    plt.ylabel('False Positive')
    plt.show()
    print('1')





def ShowDifferenceBetweenTests(TestsWithInfo):
    stress1Data=TestsWithInfo.loc[TestsWithInfo['video']=='stress1']
    stress2Data=TestsWithInfo.loc[TestsWithInfo['video']=='stress2']
    calmData=TestsWithInfo.loc[TestsWithInfo['video']=='calm']
    
    showDiffGraph(stress1Data, stress2Data, 'Differance Between Stress1 And Stress2')

def showDiffGraph(stress1Data, stress2Data, title):
    diff=pd.DataFrame(columns=['FN', 'picFN', 'wordFN', 'faceFN','FP', 'picFP', 'wordFP', 'faceFP', 'TN', 'picTN', 'wordTN', 'faceTN','TP', 'picTP', 'wordTP', 'faceTP'])

    for index, row in stress1Data.iterrows():
        row2=stress2Data.loc[stress2Data['userId']==row['userId']].iloc[[0]]


    ShowFalsePositiveGraphs(diff)

def GraphForColumns(xColumn, yColumn, DF):
    averageDF=DF.groupby(xColumn).mean()
    plt.plot(averageDF.index, averageDF[yColumn])
    plt.show()





