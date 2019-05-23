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
    CalmData=TestsWithInfo.groupby('PositiveLevel').mean()
    plt.plot(CalmData.index, CalmData['FP'])
    plt.plot(CalmData.index, CalmData['picFP'])
    plt.plot(CalmData.index, CalmData['wordFP'])
    plt.plot(CalmData.index, CalmData['faceFP'])
    plt.legend(['Averaged False Positive', 'Pictures False Positive', 'Words False Positive', 'Faces False Positive'], loc='upper left')
    plt.title('Stress Level - False Positive')
    plt.xlabel('Stress Level')
    plt.ylabel('False Positive')
    plt.show()

    # NegativeLevel Graph
    # FP
    # CalmData = TestsWithInfo.groupby('PositiveLevel').mean()
    # plt.plot(CalmData.index, CalmData['FP'])
    # plt.plot(CalmData.index, CalmData['picFP'])
    # plt.plot(CalmData.index, CalmData['wordFP'])
    # plt.plot(CalmData.index, CalmData['faceFP'])
    # plt.legend(['Averaged False Positive', 'Pictures False Positive', 'Words False Positive', 'Faces False Positive'],
    #            loc='upper left')
    # plt.title('Positive Level - False Positive')
    # plt.xlabel('Positive Level')
    # plt.ylabel('False Positive')
    # plt.show()
    print('1')

def GraphByQuestionType(Data):
    calmData=Data.loc[Data['video']=='calm']
    stress1Data=Data.loc[Data['video']=='stress1']
    stress2Data=Data.loc[Data['video']=='stress2']
    # words
    wordsCalm=calmData.groupby('CalmLevel').mean()
    wordsStress1=stress1Data.groupby('CalmLevel').mean()
    wordsStress2=stress2Data.groupby('CalmLevel').mean()
    plt.plot(wordsCalm.index, wordsCalm['wordFP'])
    plt.plot(wordsStress1.index, wordsStress1['wordFP'])
    plt.plot(wordsStress2.index, wordsStress2['wordFP'])

    plt.legend(['Calm FP', 'Stress1 FP', 'Stress2 FP'],
               loc='upper left')
    plt.title('Stress Level - False Positive In Word Questions')
    plt.xlabel('Stress Level')
    plt.ylabel('False Positive')
    plt.show()
    print('1')

    # pic
    plt.clf()
    plt.plot(wordsCalm.index, wordsCalm['picFP'])
    plt.plot(wordsStress1.index, wordsStress1['picFP'])
    plt.plot(wordsStress2.index, wordsStress2['picFP'])

    plt.legend(['Calm FP', 'Stress1 FP', 'Stress2 FP'],
               loc='upper left')
    plt.title('Stress Level - False Positive In Pictures Questions')
    plt.xlabel('Stress Level')
    plt.ylabel('False Positive')
    plt.show()
    print('1')

    # pic
    plt.clf()
    plt.plot(wordsCalm.index, wordsCalm['faceFP'])
    plt.plot(wordsStress1.index, wordsStress1['faceFP'])
    plt.plot(wordsStress2.index, wordsStress2['faceFP'])

    plt.legend(['Calm FP', 'Stress1 FP', 'Stress2 FP'],
               loc='upper left')
    plt.title('Stress Level - False Positive In Pictures Faces')
    plt.xlabel('Stress Level')
    plt.ylabel('False Positive')
    plt.show()
    print('1')

    # pic
    plt.clf()
    plt.plot(wordsCalm.index, wordsCalm['FP'])
    plt.plot(wordsStress1.index, wordsStress1['FP'])
    plt.plot(wordsStress2.index, wordsStress2['FP'])

    plt.legend(['Calm FP', 'Stress1 FP', 'Stress2 FP'],
               loc='upper left')
    plt.title('Stress Level - Average False Positive In All Questions')
    plt.xlabel('Stress Level')
    plt.ylabel('False Positive')
    plt.show()
    print('1')






def ShowDifferenceBetweenTests(TestsWithInfo):
    stress1Data=TestsWithInfo.loc[TestsWithInfo['video']=='stress1']
    stress2Data=TestsWithInfo.loc[TestsWithInfo['video']=='stress2']
    calmData=TestsWithInfo.loc[TestsWithInfo['video']=='calm']
    
    diffDF=findDiff(calmData, stress1Data)
    ShowFalsePositiveGraphs(diffDF)

def findDiff(stress1Data, stress2Data):
    # diff=pd.DataFrame(columns=['FN', 'picFN', 'wordFN', 'faceFN','FP', 'picFP', 'wordFP', 'faceFP', 'TN', 'picTN', 'wordTN', 'faceTN','TP', 'picTP', 'wordTP', 'faceTP'])

    # merged=pd.merge(stress1Data,stress2Data,on=['userId'], how='inner')
    stress1Data=stress1Data.reset_index()
    stress2Data=stress2Data.reset_index()
    stress1Data=stress1Data.set_index('userId')
    stress2Data=stress2Data.set_index('userId')
    stress1Data=stress1Data.drop(['index','testId', 'video', 'age','gender','englishLevel', 'hand'], axis=1)
    stress2Data=stress2Data.drop(['index','testId', 'video', 'age','gender','englishLevel', 'hand'], axis=1)
    diff=stress2Data.subtract(stress1Data)
    return diff
    # diff['FN']=merged['FN_x']-merged['FN_y']
    # diff['picFN']=merged['picFN_x']-merged['picFN_y']
    # diff['wordFN']=merged['wordFN_x']-merged['wordFN_y']
    # diff['faceFN']=merged['faceFN_x']-merged['faceFN_y']
    # diff['FP']=merged['FP_x']-merged['FP_y']
    # diff['picFP']=merged['picFP_x']-merged['picFP_y']
    # diff['wordFP']=merged['wordFP_x']-merged['wordFP_y']
    # diff['faceFP']=merged['faceFP_x']-merged['faceFP_y']
    # diff['wordFP']=merged['wordFP_x']-merged['wordFP_y']
    # diff['TN']=merged['TN_x']-merged['TN_y']
    # diff['picTN']=merged['picTN_x']-merged['picTN_y']
    # diff['wordTN']=merged['wordTN_x']-merged['wordTN_y']
    # diff['faceTN']=merged['faceTN_x']-merged['faceTN_y']
    # diff['TP']=merged['TP_x']-merged['TP_y']
    # diff['picTP']=merged['picTP_x']-merged['picTP_y']
    # diff['wordTP']=merged['wordTP_x']-merged['wordTP_y']
    # diff['faceTP']=merged['faceTP_x']-merged['faceTP_y']
    # diff['diffCalm']=merged['diffCalm_x']-merged['diffCalm_y']
    # diff['diffHappy']=merged['diffHappy_x']-merged['diffHappy_y']
    # diff['CalmLevel']=merged['CalmLevel_x']-merged['CalmLevel_y']
    # diff['PositiveLevel']=merged['PositiveLevel_x']-merged['PositiveLevel_y']
    # diff['userId']=merged['userId']
    # diff['faceTP']=merged['faceTP_x']-merged['faceTP_y']

    # for index, row in stress1Data.iterrows():
    #     row2=stress2Data.loc[stress2Data['userId']==row['userId']].iloc[[0]]


    ShowFalsePositiveGraphs(diff)

def GraphForColumns(xColumn, yColumn, DF):
    averageDF=DF.groupby(xColumn).mean()
    plt.plot(averageDF.index, averageDF[yColumn])
    plt.show()





