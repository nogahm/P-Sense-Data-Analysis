import PreProcess
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("whitegrid")


import pandas as pd
import numpy as np

def ShowFalsePositiveGraphs():
    TestsWithInfo=PreProcess.TestsWithScores.copy()
    # change diff calm for graph - bigger diff=more stress
    TestsWithInfo['diffCalm']=TestsWithInfo['diffCalm']*(-1)
    # for each diffCalm - average of all other columns
    diffCalmAVG=TestsWithInfo.groupby('diffCalm').mean()
    # FP and change in calm - Graph
    # plt.plot(diffCalmAVG.index, diffCalmAVG['falsePositive'])
    # plt.show()

    # for each diffHappy - average of all other columns
    # diffHappyAVG=TestsWithInfo.groupby('diffHappy').mean()
    # plt.plot(diffHappyAVG.index, diffHappyAVG['falsePositive'])
    # plt.show()
    GraphForColumns('CalmLevel','falsePositive',TestsWithInfo)
    print('1')

def GraphForColumns(xColumn, yColumn, DF):
    averageDF=DF.groupby(xColumn).mean()
    plt.plot(averageDF.index, averageDF[yColumn])
    plt.show()





