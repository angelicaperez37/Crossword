import sys
import os.path
from util import *
from classes import *
import random
from datetime import datetime
from search import *
from grid import *
from feature import *
from learning import *
from csp import *
from ast import literal_eval as make_tuple

start = timeit.default_timer()

#Globals
cwSize = 9
numFeatures = 6
dataFileName = 'trainingMidiResults_trial6_delta_weight_scores_500iter_wbw.txt'
weightFileName = 'weights_midi_trial6_delta_weight_scores_500iter_wbw.txt'

# Process Database
d = createGoogleDatabase()   #createNYTDatabase
sortedData = sortDatabase(d, cwSize) #dict where keys are the lengths of the words co								ntained in corresponding list

# Choose crossword grid pattern
grid = getMidiGrid()

# Create Crossword Object
#cw = createCrossword(size=5, sortedData=sortedData, blanks=grid)

QLA = QLearningAlgorithm(numFeatures)
iters = 500
numSolved = 0
temp = datetime.now()
totalTime = temp-temp
totalAccuracy = 0.0
for i in range(iters):

	solved = False
	print 'Iteration ' + str(i+1)

	print 'Creating Crossword object'
	cw = createCrossword(size=cwSize, sortedData=sortedData, blanks=grid)

	print 'Creating CSP'
	csp = createCrosswordCSP(cw)
	start = datetime.now()

	print 'In Backtrack Search'
	search = BacktrackingSearch()
	solution, fvs, domainPercentages, assignments, reason = search.solve(cw, csp, mcv=False, ac3=True)
	print 'Terminated because : ' + reason
	end = datetime.now()
	addAssignmentsToGrid(cw, solution)

	print 'Incorporating feedback.'
	# Compute Puzzle correctness
	numWordsAssigned = 0
	for var in solution.keys():
		if len(make_tuple(var)) > 2:
			numWordsAssigned += 1
	solvedPerc = numWordsAssigned*1.0/len(cw.words.keys())
	QLA.incorporateFeedback(fvs, assignments, domainPercentages, solvedPerc)
	wf = open(weightFileName, 'wb')
	for j in range(26):
		QLA.weights[j].tofile(wf, "\n")
	wf.close()

	print solution
	print domainPercentages
	print solvedPerc

	print cw.grid

	totalTime += (end-start)
	totalAccuracy += solvedPerc

	if len(solution.keys()) == csp.numVars:
		numSolved += 1
		solved = True

	# For logging experimental results
	df = open(dataFileName, 'a')
	toWrite = '\nATTEMPT ' + str(i+1) +	'\nAccuracy: ' + str(solvedPerc) + '\nAccuracy so far: ' + str(totalAccuracy*1.0/(i+1)) + '\nSearch time: '+ str(end-start) + '\nAverage time: ' +str(totalTime/(i+1)) + '\n'
	df.write(toWrite)
	df.close()
	df = open(dataFileName, 'ab')
	cw.grid.tofile(df, " ")
	df.close()
	print toWrite

print QLA.weights
df = open(dataFileName, 'a')
df.write("Solved "+str(numSolved)+" out of "+str(i+1)+" puzzles \n")
df.close()

###
#features = CWFeatureExtractor(cw, cw.letters[(0,2)], 'A')
#print features
