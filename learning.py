import collections
import math

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


