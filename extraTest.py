import sys
import os.path
from util import *
from classes import *
import random 
from datetime import datetime
from search import *

start = timeit.default_timer()

# Process Database
d = createClueDatabase()
sortedData = sortDatabase(d, 5) #dict where keys are the lengths of the words co								ntained in corresponding list

for clue in sortedData[5]:
	if 'III' in clue[1]:
		print clue
		exit()
exit()

# Create CSP Model
csp = createCrosswordCSP(size=5, sortedData=sortedData)

#Choose order of variable placement
order = computeVariableOrdering(csp)

# Solve Board
numSolved = 0

# For logging experimental results
dataFileName = 'basicSearch.txt'
dataFile = open(dataFileName, 'a')
dataFile.write('Run')

for i in range(25):
	csp = createCrosswordCSP(size=5, sortedData=sortedData)
	start = datetime.now()

	solved = basicSearch(sortedData, csp, order)

	end = datetime.now()
	toWrite = 'ATTEMPT ' + str(i) +	'\nSolved: ' + str(solved) + '\nSearch time: '+ str(end-start) + '\n' + str(start) + '\n' + str(end) 

	print toWrite
	dataFile.write(toWrite)

	if solved:	numSolved += 1

print str(numSolved) + ' puzzles Solved.\n'
print 'Accuracy: ' + str(numSolved/25.0)


