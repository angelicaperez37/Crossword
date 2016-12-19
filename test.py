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
numFeatures = 70
dataFileName = 'temp_testingMidiResults_trial5.txt'
#weightFileName = 'weights_midi_trial1.txt'

# Process Database
d = createGoogleDatabase()   #createNYTDatabase
sortedData = sortDatabase(d, cwSize) #dict where keys are the lengths of the words co								ntained in corresponding list

# Choose crossword grid pattern
grid = getMidiGrid()

# Get training weights from datafile
lineNum = 0
weights = np.matrix([[0.0] * numFeatures]*26)
for line in open('weights_midi_trial5_delta_weight_scores_500iter.txt'):
	row = lineNum/numFeatures
	col = lineNum%numFeatures
	weights[row,col] = float(line)
	lineNum += 1

# Create Crossword Object
#cw = createCrossword(size=5, sortedData=sortedData, blanks=grid)

iters = 100
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
	solution = search.solve_test(weights, cw, csp, mcv=True, ac3=True)
	end = datetime.now()
	addAssignmentsToGrid(cw, solution)

	print 'Computing Accuracy'
	numWordsAssigned = 0
	for var in solution.keys():
		if len(make_tuple(var)) > 2:
			numWordsAssigned += 1
	solvedPerc = numWordsAssigned*1.0/len(cw.words.keys())

	print solution
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

df = open(dataFileName, 'a')
df.write("Solved "+str(numSolved)+" out of "+str(i+1)+" puzzles \n")
df.close()

###
#features = CWFeatureExtractor(cw, cw.letters[(0,2)], 'A')
#print features
