# Analysis Script

# Algorithm Analysis
	# Cohort A - varied memory depth
		# Group 1A (frequentist and puremax) - algos 1, 5, 9, 13, 17, 21, 25, 29
		# Group 2A (frequentist and softmax) - algos 2, 6, 10, 14, 18, 22, 16, 30
		# Group 3A (Bayesian and puremax) - algos 3, 7, 11, 15, 19, 23, 27, 31
		# Group 4A (Bayesian and softmax) - algos 4, 8, 12, 16, 20, 24, 28, 32
	# Cohort B - varied statistics method
		# Group 1B (d = 2 and puremax) - algos 1 and 3
		# Group 2B (d = 2 and softmax) - algos 2 and 4
		# Group 3B (d = 4 and puremax) - algos 5 and 7
		# Group 4B (d = 4 and softmax) - algos 6 and 8
		# Group 5B (d = 8 and puremax) - algos 9 and 11
		# Group 6B (d = 8 and softmax) - algos 10 and 12
		# Group 7B (d = 16 and puremax) - algos 13 and 15
		# Group 8B (d = 16 and softmax) - algos 14 and 16
		# Group 9B (d = 32 and puremax) - algos 17 and 19
		# Group 10B (d = 32 and softmax) - algos 18 and 20
		# Group 11B (d = 64 and puremax) - algos 21 and 23
		# Group 12B (d = 64 and softmax) - algos 22 and 24
		# Group 13B (d = 128 and puremax) - algos 25 and 27
		# Group 14B (d = 128 and softmax) - algos 26 and 28
		# Group 15B (d = 256 and puremax) - algos 29 and 31
		# Group 16B (d = 256 and softmax) - algos 30 and 32
	# Cohort C - varied decision policy
		# Group 1C (d = 2 and frequentist) - algos 1 and 2
		# Group 2C (d = 2 and Bayesian) - algos 3 and 4
		# Group 3C (d = 4 and frequentist) - algos 5 and 6
		# Group 4C (d = 4 and Bayesian) - algos 7 and 8
		# Group 5C (d = 8 and frequentist) - algos 9 and 10
		# Group 6C (d = 8 and Bayesian) - algos 11 and 12
		# Group 7C (d = 16 and frequentist) - algos 13 and 14
		# Group 8C (d = 16 and Bayesian) - algos 15 and 16
		# Group 9C (d = 32 and frequentist) - algos 17 and 18
		# Group 10C (d = 32 and Bayesian) - algos 19 and 20
		# Group 11C (d = 64 and frequentist) - algos 21 and 22
		# Group 12C (d = 64 and Bayesian) - algos 23 and 24
		# Group 13C (d = 128 and frequentist) - algos 25 and 26
		# Group 14C (d = 128 and Bayesian) - algos 27 and 28
		# Group 15C (d = 256 and frequentist) - algos 29 and 30
		# Group 16C (d = 256 and Bayesian) - algos 31 and 32
		
	# Each group will be independently t-tested on each mab to count number of significant differences (20 mabs per group)
		# Comparing absolute score, regret, and decision consistency


import pandas as pd
from scipy.stats import ttest_ind_from_stats

#df = pd.read_csv('clean_results.csv')
#df.to_json('clean_results.json')

df = pd.read_json('clean_results.json')


# calculate p-values between two algo performances

def tTestForSigDiff(algo1Stats, algo2Stats):
	
#	print(type(algo1Stats))
	
#	print(type(int(algo1Stats[0])))
	
	significantDifferences = [] # will return 3 boolean values
	
	if ttest_ind_from_stats(algo1Stats[0], algo1Stats[1], 100, algo2Stats[0], algo2Stats[1], 100).pvalue < 0.01:
		significantDifferences.append(True)
	else:
		significantDifferences.append(False)
		
	if ttest_ind_from_stats(algo1Stats[2], algo1Stats[3], 100, algo2Stats[2], algo2Stats[3], 100).pvalue < 0.01:
		significantDifferences.append(True)
	else:
		significantDifferences.append(False)
		
	if ttest_ind_from_stats(algo1Stats[4], algo1Stats[5], 100, algo2Stats[4], algo2Stats[5], 100).pvalue < 0.01:
		significantDifferences.append(True)
	else:
		significantDifferences.append(False)
		
#	print(significantDifferences)
		
	return significantDifferences


# count significant differences on all mabs for two algos within a group
	# algos are indexed 0-31

def countAlgoSigDiff(algoIndex1, algoIndex2, resultDf):
	
	sigDiffCount = [0, 0, 0, 20] # 4 integers - count of sigDiffs in absolute score, regret, decision consistency, and total tests
	
	for i in range(20): # 20 mabs to test
		sigDiffs = tTestForSigDiff(resultDf['mab' + str(i + 1)][algoIndex1], resultDf['mab' + str(i + 1)][algoIndex2])
		for j in range(len(sigDiffs)):
			if sigDiffs[j]:
				sigDiffCount[j] += 1
				
	return sigDiffCount


# calls countAlgoSigDiff() on all algo groups in cohort A -- 4 groups of 8

def algoCohortA(resultDf):
	
	# key - group number, value - list of significant differences for each measure
	sigDiffDict = {}
	
	for i in range(4): # 4 test groups
		sigDiffCount = [0, 0, 0, 0] # reset to zero for each group
		for j in range(7): # test each combination within group
			for k in range(7):
				if j + k <= 6:
					sigDiffs = countAlgoSigDiff((j * 4) + i, (j * 4) + (k * 4) + 4 + i, resultDf)
					for l in range(len(sigDiffs)):
						sigDiffCount[l] += sigDiffs[l]
		sigDiffDict['Group ' + str(i + 1)] = sigDiffCount
		print('Algo Cohort A, Group ' + str(i + 1) + ' analysis complete.')
	
	return sigDiffDict


# calls countAlgoSigDiff() on all algo groups in cohort B -- 16 groups of 2

def algoCohortB(resultDf):
	
	# key - group number, value - list of significant differences for each measure
	sigDiffDict = {}
	
	for i in range(16): # 16 test groups
		if i % 2 == 0:
			sigDiffs = countAlgoSigDiff(i * 2, (i * 2) + 2, resultDf)
		else:
			sigDiffs = countAlgoSigDiff((i * 2) - 1, (i * 2) + 1, resultDf)
		sigDiffDict['Group ' + str(i + 1)] = sigDiffs
		print('Algo Cohort B, Group ' + str(i + 1) + ' analysis complete.')
		
	return sigDiffDict


# calls countAlgoSigDiff() on all algo groups in cohort C -- 16 groups of 2

def algoCohortC(resultDf):
	
	# key - group number, value - list of significant differences for each measure
	sigDiffDict = {}
	
	for i in range(16): # 16 test groups
		sigDiffs = countAlgoSigDiff(i * 2, (i * 2) + 1, resultDf)
		sigDiffDict['Group ' + str(i + 1)] = sigDiffs
		print('Algo Cohort C, Group ' + str(i + 1) + ' analysis complete.')

	return sigDiffDict


# counts significant differences on algo performances between two mabs

def countMabSigDiff(mab1Index, mab2Index, resultDf):
	
	sigDiffCount = [0, 0, 0, 32]
	
	for i in range(32): # 32 algos to test
		sigDiffs = tTestForSigDiff(resultDf[mab1Index][i], resultDf[mab2Index][i])
		for j in range(len(sigDiffs)):
			if sigDiffs[j]:
				sigDiffCount[j] += 1
				
	return sigDiffCount


# calls countMabSigDiff() on all groups in cohort A -- 4 groups of 2 (test task and control task)

def mabCohortA(resultDf):
	
	# key - group number, value - list of significant differences for each measure
	sigDiffCount = {}
	
	for i in range(4): # 4 test groups
		sigDiffs = countMabSigDiff('mab1', 'mab' + str(i + 2), resultDf)
		sigDiffCount['Group ' + str(i + 1)] = sigDiffs
		print('Mab Cohort A, Group ' + str(i + 1) + ' analysis complete.')
	
	return sigDiffCount


# calls countMabSigDiff() on all groups in cohort B -- 2 groups of 2 (not compared w/ control task)

def mabCohortB(resultDf):
	
	# key - group number, value - list of significant differences for each measure
	sigDiffCount = {}
	
	for i in range(2): # 2 test groups
		sigDiffs = countMabSigDiff('mab' + str(i + 2), 'mab' + str(i + 4), resultDf)
		sigDiffCount['Group ' + str(i + 1)] = sigDiffs
		print('Mab Cohort B, Group ' + str(i + 1) + ' analysis complete.')
	
	return sigDiffCount


# calls countMabSigDiff() on all groups in cohort C -- 2 groups of 5 

def mabCohortC(resultDf):

	# key - group number, value - list of significant differences for each measure
	sigDiffDict = {}
	
	for i in range(2): # 2 test groups
		sigDiffCount = [0, 0, 0, 0] # reset to zero for each group
		for j in range(4): # test each combination within group
			for k in range(4):
				if j + k <= 3:
					if j == 0:
						sigDiffs = countMabSigDiff('mab6', 'mab' + str(k + 7 + (i * 4)), resultDf)
					else:
						sigDiffs = countMabSigDiff('mab' + str(j + 6 + (i * 4)), 'mab' + str(j + 7 + k + (i * 4)), resultDf)
					for l in range(len(sigDiffs)):
						sigDiffCount[l] += sigDiffs[l]
		sigDiffDict['Group ' + str(i + 1)] = sigDiffCount
		print('Mab Cohort C, Group ' + str(i + 1) + ' analysis complete.')

	return sigDiffDict


# calls countMabSigDiff() on all groups in cohort D -- 2 groups of 4

def mabCohortD(resultDf):
	
	# key - group number, value - list of significant differences for each measure
	sigDiffDict = {}
	
	for i in range(2): # 2 test groups
		sigDiffCount = [0, 0, 0, 0] # reset to zero for each group
		for j in range(3): # test each combination within group
			for k in range(3):
				if j + k <= 2:
					if j == 0:
						sigDiffs = countMabSigDiff('mab' + str(6 + i), 'mab' + str(k + 15 + i), resultDf)
					else:
						sigDiffs = countMabSigDiff('mab' + str((j * 2) + 13 + i), 'mab' + str((k * 2) + 15 + i), resultDf)
					for l in range(len(sigDiffs)):
						sigDiffCount[l] += sigDiffs[l]
		sigDiffDict['Group ' + str(i + 1)] = sigDiffCount
		print('Mab Cohort D, Group ' + str(i + 1) + ' analysis complete.')
	
	return sigDiffDict







'''
	Analysis.learningRate()
----------------------------------------
Parameters: taskData dictionary
Returns: taskData w/ added column
'switched', as well as the learning rate
----------------------------------------

'''

def learningRate(taskData):
	
	switched_data = [1]
	rowLabels = []
	
	for row in range(1, len(taskData['Decisions'])):
		if taskData['Decisions'][row + 1] != taskData['Decisions'][row]:
			switched_data.append(1)
		else:
			switched_data.append(0)
		rowLabels.append(row)
	
	s = pd.Series(switched_data, rowLabels)
	taskData['Data']['Switched'] = s
	taskData['Learning Rate'] = sum(switched_data) / len(switched_data)
	
	return taskData




'''
		Analysis.regret()
-------------------------------------
Parameters: taskData dictionary
Returns: taskData DataFrame w/ added
columns 'Step Regret' and 'Cumulative
Regret', as well as the optimal score
-------------------------------------

'''

def regret(taskData):
	
	optimalOutcome = taskData['Task'].getOptimal()
	stepRegret = []
	cumRegret = []
	rowLabels = []
	
	for row in range(1, len(taskData['Outcomes']) + 1):
		stepRegret.append(optimalOutcome - taskData['Outcomes'][row])
		cumRegret.append(sum(stepRegret))
		rowLabels.append(row)
	
	s1 = pd.Series(stepRegret, rowLabels)
	s2 = pd.Series(cumRegret, rowLabels)
	taskData['Data']['Step Regret'] = s1
	taskData['Data']['Cumulative Regret'] = s2
	taskData['Optimal Score'] = optimalOutcome * taskData['Trials']
	
	return taskData