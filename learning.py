import collections
import math
import numpy as np

class QLearningAlgorithm():

	def __init__(self, numFeatures):
		self.weights = np.matrix([[0] * numFeatures]*26)
		# to get letter var's weight vector:
			# rowIdx = string.ascii_uppercase.index('[letter]')
			# self.weights[rowIdx]
		self.initDomainSizes = domainSizes
		self.stepSize = 0.1
		self.discount = 1


	''' performs Q-learning on a single CSP assignment by updating weights.
	# @featureVecs : dict of int keys and dict values
	#	- keys are the assignment orders
	#	- dict values hold the feature vectors for all possible assignments
	# @assignments : dict with int keys and letter/variable values
	# @maxFeatureVecs: dict with int keys and max feature vec lists
	'''
	def incorporateFeedback(self, featureVecs, assignments, domainPerc, solved):
		for t in range(len(assignments.keys())):
			a = assignments[t]
			wRowIdx = string.ascii_uppercase.index(a)
			reward = computeReward(domainPerc[t], solved)
			target = np.multiply(findMaxQ(featureVecs[t]),self.discount)+reward
			prediction = np.multiply(self.weights[rowIdx], featureVecs[t][a])
			temp = np.multiply(target-prediction, featureVecs[t][a])
			self.weights[rowIdx] += np.multiply(temp, self.stepSize)

	def computeReward(domainPerc, solved):
		reward = domainPerc
		if solved:
			reward += 1
		return reward

	def findMaxQ(featureVecs):
		return max[np.multiply(self.weights[x], featureVecs[x]) for x in featureVecs.keys()]

'''
class QLearningAlgorithm():

	def __init__(self, varOrdering, discount, featureExtractor, explorationProb=0.2):
		self.varOrdering = varOrdering
		self.discount = discount
		self.featureExtractor = featureExtractor
		self.explorationProb = explorationProb
		self.weights = collections.Counter()
		self.numIters = 0

	def getQ(self, cw, letterVar, assignment):
		score = 0
		for f,v in self.featureExtractor(cw, letterVar, assignment):
			score += self.weights[f] * v
		return score

	def getAction(self, cw, state, letterVar):
		self.numIters += 1
		if random.random() < self.explorationProb:
			return random.choice(letterVar.domain) #TODO: CHECK
		else:
			return max((self.getQ(cw, letterVar, action), action) for action in letterVar.domain)[1]

	def getStepSize(self):
		return 1.0/math.sqrt(self.numIters)

	def incorporateFeedback(self, cw, state, letterVar, action, reward, newState):
		# check for end state
		if len(newState) == 0:
			return

		Vopt = max([self.getQ(cw, letterVar, action) for action in letterVar.domain])
		Qopt = self.getQ(cw, letterVar, action)
'''
