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
cwSize = 5
numWordFeatures = 0
numLetterFeatures = 16
dataFileName = 'trainingMiniResults_trial10_delta_weight_scores_5000iter_wbw.txt'
#weightFileName_Word = 'weights_midi_trial10_delta_weight_scores_500iter_word.txt'
weightFileName_Letter = 'weights_mini_trial10_delta_weight_scores_5000iter_letter.txt'

# Process Database
d = createGoogleDatabase()   #createNYTDatabase
sortedData = sortDatabase(d, cwSize) #dict where keys are the lengths of the words co								ntained in corresponding list

# Choose crossword grid pattern
grid = getMiniGrid()

# Create Crossword Object
#cw = createCrossword(size=5, sortedData=sortedData, blanks=grid)

QLA = QLearningAlgorithm(numWordFeatures, numLetterFeatures)
iters = 1
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
	fvs, actions, maxAdditionalAssignments = search.solve_backtrack_learning(csp, cw, mcv=True, mac=True)
	end = datetime.now()
	#addAssignmentsToGrid(cw, solution)

	#print solution
	#print cw.grid

	print 'Incorporating feedback.'
	# Compute Puzzle correctness


	QLA.incorporateFeedback_backtrack(fvs, actions,maxAdditionalAssignments)
	'''wf = open(weightFileName_Word, 'wb')
	QLA.word_weights[0].tofile(wf, "\n")
	wf.close()
	'''
	wf = open(weightFileName_Letter, 'wb')
	for j in range(26):
		QLA.weights[j].tofile(wf, "\n")
	wf.close()

	# Print results to file
	'''
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
	'''

# Print results to flle
'''
df = open(dataFileName, 'a')
df.write("Solved "+str(numSolved)+" out of "+str(i+1)+" puzzles \n")
df.close()
'''
###
#features = CWFeatureExtractor(cw, cw.letters[(0,2)], 'A')
#print features
