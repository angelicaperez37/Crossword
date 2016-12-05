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
sortedData = sortDatabase(d, 5) #dict where keys are the lengths of the words co								ntained in corresponding list

# Choose crossword grid pattern
grid = getMiniGrid()

# Create Crossword Object
cw = createCrossword(size=5, sortedData=sortedData, blanks=grid)

#addSeedWords(cw)

csp = createCrosswordCSP(cw)

search = BacktrackingSearch()
solution = search.solve(csp, mcv=False, ac3=True)
addAssignmentToGrid(cw, solution)
print cw.grid

'''for var in csp.variables:
	tup = make_tuple(var)


	if len(tup) == 2:
		print var
		print len(csp.values[var])


	if len(tup) == 2 and len(csp.values[var]) == 1:
		print var
		print csp.values[var][0]

		letter = cw.letters[tup]
		assignLetter(cw, letter, csp.values[var][0])
	elif len(csp.values[var]) == 1:
		word = cw.words[tup]
		assignWord(cw, word, csp.values[var][0])
print cw.grid
'''

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
