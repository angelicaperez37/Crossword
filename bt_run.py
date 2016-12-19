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
dataFileName = 'temp_bt_mini.txt'

# Process Database
d = createGoogleDatabase()   #createNYTDatabase
sortedData = sortDatabase(d, cwSize) #dict where keys are the lengths of the words co								ntained in corresponding list

# Choose crossword grid pattern
grid = getMiniGrid()

# Create Crossword Object
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
    search.solve(csp, cw, mcv=True, mac=True)
    end = datetime.now()
    print search.optimalAssignment
    print search.numOptimalAssignments
    print search.numAssignments
    solutions = search.allAssignments
    numOperations = search.numOperationsToFirst

    for i in range(len(solutions)):
        solution = solutions[i]
        cw.grid[:] = '*'
        addAssignmentsToGrid(cw, solution[i])

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
        df.write(str(numOperations))
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
