import sys
import os.path
from util import *
from classes import *
import random
from datetime import datetime
from search import *
from grid import *
from feature import *

start = timeit.default_timer()

# Process Database
d = createClueDatabase()
sortedData = sortDatabase(d, 9) #dict where keys are the lengths of the words co								ntained in corresponding list
# Choose crossword grid pattern
grid = getMiniGrid()
#computeVariableOrderingLetterByLetter(csp)
# getMidiGrid()

# Create Crossword Object
cw = createCrossword(size=5, sortedData=sortedData, grid=grid)
csp = createCrosswordCSP(cw)

print 'Created CrosswordCSP'
print 'numVars = '+str(csp.numVars)
print 'variables = '+str(csp.variables)
print csp.binaryFactors


###
#features = CWFeatureExtractor(cw, cw.letters[(0,2)], 'A')
#print features

# Create MDP instance
#mdp = CrosswordMDP(cw, grid)


# Solve Board
'''numSolved = 0

# For logging experimental results
dataFileName = 'basicSearchLetterByLetter.txt'
dataFile = open(dataFileName, 'a')

for i in range(25):
	csp = createCrosswordCSP(size=9, sortedData=sortedData)
	chooseSeedWord(csp, (2,0,1))
	chooseSeedWord(csp, (0,2,0))
	start = datetime.now()

	solved = basicLetterByLetterSearch(sortedData, csp, order)

	end = datetime.now()
	toWrite = 'ATTEMPT ' + str(i) +	'\nSolved: ' + str(solved) + '\nSearch time: '+ str(end-start) + '\n'

	print toWrite

	dataFile.write(toWrite)
	dataFile.write(csp.grid)

	if solved:	numSolved += 1

dataFile.write(str(numSolved) + ' puzzles Solved.\n')
dataFile.write('Accuracy: ' + str(numSolved/25.0))
'''
