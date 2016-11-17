from util import *
from classes import *
import collections, random
from grid import *
from asyncio import Queue
import copy

'''class MDP:
	def startState(self): raise NotImplementedError("Override me")
	def actions(self, state): raise NotImplementedError("Override me")
	def succAndProbReward(self, state, action): raise NotImplementedError("Override me")
	def discount(self): raise NotImplementedError("Override me")
	# Computes set of all possible states for all actions
	def computeStates(self): raise NotImplementedError("Override me")
'''


# Letter by Letter Approach
class CrosswordMDP():

	def __init__(self, cw):
		self.cw

	# returns all Letter variables
	def startState(self):	return (self.cw, self.cw.letters[self.cw.emptyLetterLocations[0]])

	# returns all unassigned Letter variables
	#def varOrdering(self, state): return 

	# returns set of all actions (or assignments) possible from sttate
	def actions(self, state):	return state[1].domain

	# returns (newState, prob, reward) for choosing action on state
	# Currently using reward (1):
	# possible rewards:
	#	1) mean of overlapping word domains after propogation
	#	2) total size of overlapping word domains after propogation
	#	3) (1) + SolvedReward
	#	4) (2) + Solved Reward
	#	5) Combos w/ OriginalityReward(TBD)
	def succAndProbRewards(self, state, action):
		letterVar = state[1]

		# if all Letter variables have been assigned
		if letterVar == None:	return []

		dom = letterVar.domain
		# if the letterVar's domain is empty
		if len(dom) == 0:	return []

		# compute new state (cw, nextVar)
		reward, newCW = computeReward(state[0], letterVar, action)

		return (

	# Returns all possible resulting states after a chosen action(Letter Assignment)
	'''def computeStates(self):
		states = []
		for L in self.cw.emptyLetterLocations:
			newState = copy.deepcopy(self.cw.emptyLetterLocations)
			states.append(newState.remove(L))
		return states
	'''
# Returns the mean of letter's overlapping Words' domains after propogation
def computeReward(cw, letter, assignment):

	newCW = copy.deepcopy(cw)
	newLetter = newCW.letters[letter.loc]
	acrossWord = newCW.words[newLetter.acrossWordLoc]
	acrossIdx = newLetter.acrossIdx	
	downWord = newCW.words[newLetter.downWordLoc]
	downIdx = newLetter.downIdx

	# Make assignment in newCW
	newLetter.assigned = True
	newLetter.assignment = assignment
	newLetter.domain = [assignment]

	# Update Word and Letter domains and compute reward
	# Overlapping Across Word
	totalDomainSize = 0	
	toRemove = []
	letterDomains = {}
	for i in range(acrossWord.length)
	for clue in acrossWord.domain:
		if clue[1][acrossIdx] == assignment:
			totalDomainSize += 1
			for i in range(acrossWord.length):
				
		else:
			toRemove.append(clue)
	for elem in toRemove:
		acrossWord.domain.remove(elem)
	# Overlapping Down Word
	toRemove = []
	for clue in downWord.domain:
		if clue[1][downIdx] == assignment:
			totalDomainSize += 1
		else:
			toRemove.append(clue)
	for elem in toRemove:
		downWord.domain.remove(elem)

	return (totalDomainSize*1.0/2, newCW)

	# TODO: DO I NEED THIS?
	# Add overlapping Words to the queue
	#for i in range(word.length):
			 



