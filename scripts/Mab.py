# MAB Class

# An instance of the MAB class is created with four parameters
	# k, an integer representing the number of arms
	# o, a list of lists representing the outcomes for each arm
	# p, a list of lists representing the outcome probabilities for each arm
	# j, a float from [0, 1] representing the jump frequency
	
# Internal methods
	# generateOutcome, a method that receives a decision input and returns an outcome
	# jump, a method that runs after every decision and determines whether or not the bandit will be restless


import random

class Mab:
	def __init__(self, arms, outcomes, probabilities, jump):
		self.k = arms
		self.o = outcomes
		self.p = probabilities
		self.j = jump
		
		
	def getArms(self):
		return self.k
	
	
	def getOptimal(self):
		
		maxEV = 0
		
		for i in range(len(self.p)):
			for j in range(len(self.p[i])):
				val = self.p[i][j] * self.o[i][j]
				if val > maxEV:
					maxEV = val

		return maxEV
	
	
	def generateOutcome(self, decision):
		
		outcome = 0
		
		outcomeSet = self.o[decision]
		probabilitySet = self.p[decision]
		
		value = random.random()
		compare = probabilitySet[0]
				
		for i in range(len(probabilitySet)):
			if value < compare:
				outcome = outcomeSet[i]
				break
			else:
				compare += probabilitySet[i + 1]
		
		self.jump(self)
		
		return outcome
	
	
	def jump(self):
		
		value = random.random()
		
		if value < self.j:
			pSet = self.p.pop(0)
			self.p.append(pSet)