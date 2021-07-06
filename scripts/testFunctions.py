# Data Collection Script

# The responsibility of the script is to instantiate and run the algorithms and their associated MABs
	# The script will utilize a pandas dataframe to store the decision & outcome data from each task
	# This data will then be condensed into metrics that describe the algorithms performance:
		# Absolute score
		# Maximum score - to be converted in maximum regret
		# Optimal score - to be converted in real regret
		# Decision consistency
		# possibly more...
	# format of JSON file:
		# Algo:
			# [depth, stats, policy]
		# Mab:
			# [arms, outcomes, probabilities, restless, frequency]
		
		
from Algorithm import Algo
from Mab import Mab
import pandas
import json
import statistics


# createObjects() reads in a JSON file and returns a list of the instantiated Algo and Mab objects

def createAlgo(jsonFile):
	
	data = 0
	
	with open(jsonFile, "r") as infile:
		data = json.load(infile)
		
	algo = Algo(data[0], data[1], data[2])
	
	return algo


def createMab(jsonFile):
	
	data = 0

	with open(jsonFile, "r") as infile:
		data = json.load(infile)
		
	mab = Mab(data[0], data[1], data[2], data[3], data[4])
	
	return mab


# runTask() plays the algo on the mab for n trials. Computes and returns 3 metrics: absolute score, regret, and decision consistency.

def runTask(algo, mab, n, s):
	
	sampleAbsoluteScore = []
	sampleRegret = []
	sampleDecisionConsistency = []
	sampleResults = []
	
	j = 0
	
	while j < s:
		
		j += 1
	
		i = 0
		decisionData = []
		outcomeData = []
		results = []
	
		optimalScore = mab.getOptimal() * n
		absoluteScore = 0
		regret = 0
		decisionConsistency = 0
	
		algo.setArms(mab.getArms())
	
		while i < n:
		
			i += 1
		
			decision = algo.makeDecision()
			outcome = mab.generateOutcome(decision)
			algo.collectResult(outcome)
		
			decisionData.append(decision)
			outcomeData.append(outcome)
		
		absoluteScore = sum(outcomeData)
		regret = optimalScore - absoluteScore
	
		decisions = [0 for i in range(len(set(decisionData)))]
	
		for i in decisionData:
			decisions[i] += 1
		
		decisionConsistency = max(decisions) / n 
	
		sampleAbsoluteScore.append(absoluteScore)
		sampleRegret.append(regret)
		sampleDecisionConsistency.append(decisionConsistency)
		
	sampleAbsoluteScoreMean = statistics.mean(sampleAbsoluteScore)
	sampleAbsoluteScoreSD = statistics.stdev(sampleAbsoluteScore)
	sampleRegretMean = statistics.mean(sampleRegret)
	sampleRegretSD = statistics.stdev(sampleRegret)
	sampleDecisionConsistencyMean = statistics.mean(sampleDecisionConsistency)
	sampleDecisionConsistencySD = statistics.stdev(sampleDecisionConsistency)
	
	sampleResults = [sampleAbsoluteScoreMean, sampleAbsoluteScoreSD, sampleRegretMean, sampleRegretSD, sampleDecisionConsistencyMean, sampleDecisionConsistencySD]
	
	return sampleResults



## regretSamples()
	# gets an algo, mab, trial number, and sample number
	# plays the algo on the mab n times
	# calculates regret of each sample
	# repeats s times
	# numpy array of sampled regret
	
def regretSamples(algo, mab, n, s):
	
	# set arms for algo
	algo.setArms(mab.getArms)
	
	# list of regret samples
	regretSample = []
	
	# collect optimal score
	optimal = mab.getOptimal() * n
	
	# s samples
	for i in range(s):
		
		# reset algo
		algo.reset()
	
		# collect absolute score
		absolute = 0
	
		# n trials
		for j in range(n):
		
			decision = algo.makeDecision()
			outcome = mab.generateOutcome(decision)
			algo.collectResult(outcome)
		
			absolute += outcome
		
		regret = round((optimal - absolute) / optimal, 6)
		regretSample.append(regret)
		
	regretSample = np.array(regretSample)