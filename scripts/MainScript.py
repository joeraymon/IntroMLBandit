# Main Script for task running, data collection, and analysis

import testFunctions
import Analysis
import csv
import pandas as pd
import numpy as np


## Run Tasks and Collect Performance Data #
#
## holds set of algo objects
#algoSet = []
#
## holds set of mab objects
#mabSet = []
#
## intermediate object to hold lists of algo performance results
#data = []
#
## intermediate object to hold a pandas series of algo performance results on each mab
#d = {}
#
## holds mab labels for resulting data frame - 'mab1', 'mab2', etc.
#rowLabels = [] 
#
## resulting pandas data frame to hold all algo performances on each mab
#resultsDf = pd.DataFrame(d) 
#
#
## instantiate 32 algo objects
#for i in range(32):
#	algoSet.append(testFunctions.createAlgo('algo' + str(i + 1) + '.txt'))
#	
## instantiate 20 mab objects
#for i in range(20):
#	mabSet.append(testFunctions.createMab('mab' + str(i + 1) + '.txt'))
#	rowLabels.append('mab' + str(i + 1))
#
## run each algo object on each mab and store performance results by first creating a series labelled by the mab and then keying to the results data frame
#for i in range(len(algoSet)):
#	data = []
#	for j in range(len(mabSet)):
#		results = testFunctions.runTask(algoSet[i], mabSet[j], 256, 100)
#		data.append(results)
#	d = pd.Series(data, rowLabels)
#	resultsDf['algo' + str(i + 1)] = d
#	print('algo' + str(i + 1) + 'complete.')
#
## transpose table for analysis
#resultsDf = resultsDf.transpose()
#
## save data frame
#resultsDf.to_pickle('real_pickled_results.csv')


# Run Cohort Group Analysis and Collect Significant Differences in Performance #

# stores significant results by cohort
sigDiffsByCohortDict = {}

# load data frame
resultsDf = pd.read_pickle('real_pickled_results.csv')

# collect and store significant differences for each group within each cohort
sigDiffsByCohortDict['Algo Cohort A'] = Analysis.algoCohortA(resultsDf)
sigDiffsByCohortDict['Algo Cohort B'] = Analysis.algoCohortB(resultsDf)
sigDiffsByCohortDict['Algo Cohort C'] = Analysis.algoCohortC(resultsDf)
sigDiffsByCohortDict['Mab Cohort A'] = Analysis.mabCohortA(resultsDf)
sigDiffsByCohortDict['Mab Cohort B'] = Analysis.mabCohortB(resultsDf)
sigDiffsByCohortDict['Mab Cohort C'] = Analysis.mabCohortC(resultsDf)
sigDiffsByCohortDict['Mab Cohort D'] = Analysis.mabCohortD(resultsDf)

print(sigDiffsByCohortDict)

# calculate significant differences counted as a percentage of total tests for each group
for cohort in sigDiffsByCohortDict:
	for group in sigDiffsByCohortDict[cohort]:
		for i in range(len(sigDiffsByCohortDict[cohort][group]) - 1):
			sigDiffsByCohortDict[cohort][group][i] = round(100 * sigDiffsByCohortDict[cohort][group][i] / sigDiffsByCohortDict[cohort][group][3], 2)
			
# create data frame for each cohort

column_labels = ['Absolute Score pct. of Sig Diffs', 'Regret pct. of Sig Diffs', 'Decision Consistency pct. of Sig Diffs', 'Total Number of Tests']

for cohort in sigDiffsByCohortDict:
	s = {}
	df = pd.DataFrame(s)
	for group in sigDiffsByCohortDict[cohort]:
		s = pd.Series(sigDiffsByCohortDict[cohort][group], column_labels)
		df[group] = s
	sigDiffsByCohortDict[cohort] = df
	df.to_csv('sigDiffCount' + str(cohort) + '.csv')