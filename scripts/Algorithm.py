# Algorithm Class

# An instance of the algorithm class is created with three parameters
	# d, an integer that represents memory depth
	# s, a boolean that represents statistics method (False - frequentist, True - Bayesian)
	# p, a boolean that represent decision policy (False - puremax, True - softmax)
	# k, an integer which represents the number of decisions that are available
	
# Internal data structures
	# wm, a list of tuples (chosen k, result) that represents the current working memory
	# pb, a list of tuples (k, expected value) that represent the prior beliefs about each decision's expected outcome
	
# Internal methods
	# calculateEV, refreshes expected values after each result
	# makeDecision, returns a k based on decision policy 
	# collectResult, received the result of the previous decision and adds to wm 
	# checkMem, called after a result is collected and removes an excess memory
	
import random
import math

class Algo:
	def __init__(self, depth, stats, policy):
		self.d = depth
		self.s = stats
		self.p = policy
		self.k = 0
		self.wm = []
		self.pb = []
		self.r = True
	

	def reset(self):
		self.wm = []
		self.pb = []

	
	def setArms(self, k):
		self.reset(self)
		self.k = k
		self.pb = [[i, 0] for i in range(k)]
		
	
	def calculateEV(self):
		
		if self.s: # Bayesian
			
			for i in self.pb:
				
				w = 0 # times arm was chosen
				x = 0 # times positive result came from arm
				y = 0 # times positive result was received
				z = 0 # total choices
				
				for j in self.wm:
					if i[0] == j[0]:
						w += 1
						if j[1] == 1:
							x += 1
					if j[1] == 1:
						y += 1
					z += 1
#				print(w)
#				print(x)
#				print(y)
#				print(z)
				if y == 0 or w == 0:
					i[1] = 0
				else:
					i[1] = ((x / y) * (y / z)) / (w / z)
					
		else: # Frequentist
		
			for i in self.pb:
				
				x = 0 # sum of score for arm
				y = 0 # number of times arm was chosen
				
				for j in self.wm:
					if i[0] == j[0]:
						x += j[1]
						y += 1
				if y == 0:
					i[1] = 0
				else:
					i[1] = x / y
				
			
	def makeDecision(self):
		
		if self.r:
			choice = random.randint(0, self.k - 1)
		
		elif self.p: # softmax
		
			pSum = 0
			distribution = []
			
			for i in self.pb:
				pSum += math.exp(i[1])
				
			for i in self.pb:
				value = math.exp(i[1]) / pSum
				distribution.append(value)
			
			value = random.random()
			comp = distribution[0]
			
			for i in range(len(distribution)):
				if value < comp:
					choice = i
					break
				else:
					comp += distribution[i + 1]
					
		else: # puremax
		
			maximum = 0
			j = 0
			
			for i in self.pb:
				if i[1] > maximum:
					maximum = i[1]
					j = i[0]
			choice = j
			
		choiceTup = [choice, 0]
		self.wm.append(choiceTup)
		return choice
		
		
	def collectResult(self, result):
		self.wm[len(self.wm) - 1][1] = result
		self.checkMem()
		self.calculateEV()
		
	def checkMem(self):
		
		if len(self.wm) > self.d:
			self.wm.pop(0)
			self.r = False
			
		if len(self.wm) == self.d:
			self.r = False
			
		if len(self.wm) == 10:
			self.r = False