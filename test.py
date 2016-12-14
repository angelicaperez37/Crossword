import sys
import os.path
from util import *
from classes import *
import random
from datetime import datetime
from search import *
from grid import *
from feature import *
from csp import *
from ast import literal_eval as make_tuple

start = timeit.default_timer()

# Process Database
d = createClueDatabase()
sortedData = sortDatabase(d, 9) #dict where keys are the lengths of the words co								ntained in corresponding list

# Choose crossword grid pattern
grid = getMidiGrid()

# Create Crossword Object
#cw = createCrossword(size=5, sortedData=sortedData, blanks=grid)

#addSeedWords(cw)
iters = 100
numSolved = 0
temp = datetime.now()
totalTime = temp-temp
for i in range(iters):
	solved = False
	print 'Iteration ' + str(i)
	cw = createCrossword(size=9, sortedData=sortedData, blanks=grid)
	csp = createCrosswordCSP(cw)
	start = datetime.now()
	search = BacktrackingSearch()
	solution = search.solve(csp, mcv=False, ac3=True)
	end = datetime.now()
	addAssignmentsToGrid(cw, solution)
	totalTime += (end-start)

	if len(solution.keys()) == csp.numVars:
		numSolved += 1
		solved = True

	# For logging experimental results
	dataFileName = 'basicMidiBacktrackSearch.txt'
	df = open(dataFileName, 'a')
	toWrite = 'ATTEMPT ' + str(i) +	'\nSolved: ' + str(solved) + '\nAccuracy so far: ' + str(numSolved*1.0/(i+1)) + '\nSearch time: '+ str(end-start) + '\nAverage time: ' +str(totalTime/(i+1)) + '\n'
	df.write(toWrite)
	df.close()
	df = open(dataFileName, 'ab')
	cw.grid.tofile(df, " ")
	df.close()

dataFileName = 'basicMidiBacktrackSearch.txt'
df = open(dataFileName, 'a')
df.write("Solved "+str(numSolved)+" out of "+str(i+1)+" puzzles \n")
df.close()

###
#features = CWFeatureExtractor(cw, cw.letters[(0,2)], 'A')
#print features
