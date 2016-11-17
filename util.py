###------------------------CROSSWORD_UTIL----------------------------###
import csv
import random
from classes import *
import string
import copy

###-----------------------DATABASE_PROCESSING------------------------###

# Reads in NYT clues and answers and stores in 'database'
def createClueDatabase():
	database = []
	with open('nyt-crossword/clues.csv','rU') as csvfile:
		rd = csv.reader(csvfile) #, delimiter = '\n',quotechar='|')
		for line in rd:
			database.append(line[0].split('\t'))

	# remove duplicates
	database.sort(key=lambda x: x[1])
	uniqueDatabase = []
	prevClue = None
	for clue in database:
		if prevClue == None:
			uniqueDatabase.append(clue)
			prevClue = clue
			continue
		elif prevClue[1] != clue[1]:
			uniqueDatabase.append(clue)
			prevClue = clue
			continue
	return uniqueDatabase

# Stores a dict of clue/word pairs sorted by length
# Dict keys: Word Length (int)
# Removes any clues with answers of length greater than maxLength
def sortDatabase(database, maxLength=25):
	database.sort(key=lambda x: len(x[1]))
	sortedData = {k: [] for k in range(maxLength+1)[3:maxLength+1]}
	for i in range(len(database)):
		clueLen = len(database[i][1])
		if clueLen > maxLength:
			break
		elif clueLen > 2:
			sortedData[clueLen].append(database[i])
	return sortedData

###---------------------------CW_UTIL---------------------------###
# Creates new Crossword Board and Variables
def createCrossword(size, sortedData, grid):
	alpha = list(string.ascii_uppercase)
	cw = Crossword(blanks=grid, size=size)
	for row in range(size):
		for col in range(size): 
			if (row,col) not in [(0,0),(1,0),(3,4),(4,4)]: #list is null squares

				# match each letter to its corresponding word
				# TO DO: decompose when add different board patterns
				acrossWordLoc = None
				downWordLoc = None
				acrossIdx = col
				downIdx = row
				if row < 2:
					acrossWordLoc = (row, 1, 1)
					acrossIdx -= 1
				else:	acrossWordLoc = (row, 0, 1)
				if col < 1:
					downWordLoc = (2, col, 0)
					downIdx -= 2
				else:	downWordLoc = (0, col, 0)

				cw.addLetter(Letter(loc=(row, col), acrossWordLoc=acrossWordLoc, acrossIdx=acrossIdx, downWordLoc=downWordLoc, downIdx=downIdx, domain=copy.deepcopy(alpha)))
				cw.addEmptyLetterLocation((row,col))
	cw.addWord((0,1,1), Word(startLoc=(0,1), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addWord((0,1,0), Word(startLoc=(0,1), length=5, across=False, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((0,2,0), Word(startLoc=(0,2), length=5, across=False, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((0,3,0), Word(startLoc=(0,3), length=5, across=False, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((0,4,0), Word(startLoc=(0,4), length=3, across=False, domain=copy.deepcopy(sortedData[3])))
	cw.addWord((1,1,1), Word(startLoc=(1,1), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addWord((2,0,1), Word(startLoc=(2,0), length=5, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((2,0,0), Word(startLoc=(2,0), length=3, across=False, domain=copy.deepcopy(sortedData[3])))
	cw.addWord((3,0,1), Word(startLoc=(3,0), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addWord((4,0,1), Word(startLoc=(4,0), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addEmptyWordLocation((0,1,0))
	cw.addEmptyWordLocation((0,1,1))
	cw.addEmptyWordLocation((0,2,0))
	cw.addEmptyWordLocation((0,3,0))
	cw.addEmptyWordLocation((0,4,0))
	cw.addEmptyWordLocation((1,1,1))
	cw.addEmptyWordLocation((2,0,1))
	cw.addEmptyWordLocation((2,0,0))
	cw.addEmptyWordLocation((3,0,1))
	cw.addEmptyWordLocation((4,0,1))
	cw.emptyLetterLocations = copy.deepcopy(cw.letters)
	cw.emptyWordLocations = copy.deepcopy(cw.words)
	return cw


# Creates new Crossword Board and Variables
def createCrosswordCSP_REPLACEMENT(size=5, sortedData=None, grid=None):
	cw = CrosswordCSP(size)
	tiles = [(x,y) for x in range(csp.size) for y in range(csp.size)]

	# Accounts for words that start on grid edges
	for i in range(size):
		if (i,0) not in grid:
			grid.append((i,-1))
		if (0,i) not in grid:
			grid.append((-1,i))

	sAcrossBlanks = sorted(grid, key=lambda x: (x[0],x[1]))
	sDownBlanks = sorted(grid, key=lambda x: (x[1],x[0]))

	# Create across Word variables
	prev = None
	for tile in sAcrossBlanks:
		if prev == None:
			prev = tile
			continue
		elif prev[0] != tile[0]:
			loc = (prev[0],prev[1]+1,1)
			cw.addWord(loc, Word(startLoc=(loc[0],loc[1]), length=size-loc[1], domain=copy.deepcopy(sortedData[size-loc[1]])))
		else:
			loc = (prev[0],prev[1]+1,1)
			cw.addWord(loc, Word(startLoc=(loc[0],loc[1]), length=tile[1]-loc[1], domain=copy.deepcopy(sortedData[tile[1]-loc[1]])))
		prev = tile

	# Create down Word variables
	prev = None
	for tile in sDownBlanks:
		if prev == None:
			prev = tile
			continue
		elif prev[1] != tile[1]:
			loc = (prev[0]+1,prev[1],0)
			cw.addWord(loc, Word(startLoc=(loc[0],loc[1]), length=size-loc[0], domain=copy.deepcopy(sortedData[size-loc[0]])))
		else:
			loc = (prev[0]+1,prev[1],0)
			cw.addWord(loc, Word(startLoc=(loc[0],loc[1]), length=tile[0]-loc[0], domain=copy.deepcopy(sortedData[tile[0]-loc[0]])))

	# LEFTOFF
	# Create Letter Variables
	alpha = list(string.ascii_uppercase)
	for row in range(size):
		for col in range(size): 
			if (row,col) not in grid: 

				# match each letter to its corresponding word
				acrossWordLoc = None
				downWordLoc = None
				acrossIdx = col
				downIdx = row
				if row < 2:
					acrossWordLoc = (row, 1, 1)
					acrossIdx -= 1
				else:	acrossWordLoc = (row, 0, 1)
				if col < 1:
					downWordLoc = (2, col, 0)
					downIdx -= 2
				else:	downWordLoc = (0, col, 0)

				cw.addLetter(Letter(loc=(row, col), acrossWordLoc=acrossWordLoc, acrossIdx=acrossIdx, downWordLoc=downWordLoc, downIdx=downIdx, domain=copy.deepcopy(alpha)))
				cw.addEmptyLetterLocation((row,col))
	cw.addWord((0,1,1), Word(startLoc=(0,1), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addWord((0,1,0), Word(startLoc=(0,1), length=5, across=False, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((0,2,0), Word(startLoc=(0,2), length=5, across=False, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((0,3,0), Word(startLoc=(0,3), length=5, across=False, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((0,4,0), Word(startLoc=(0,4), length=3, across=False, domain=copy.deepcopy(sortedData[3])))
	cw.addWord((1,1,1), Word(startLoc=(1,1), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addWord((2,0,1), Word(startLoc=(2,0), length=5, domain=copy.deepcopy(sortedData[5])))
	cw.addWord((2,0,0), Word(startLoc=(2,0), length=3, across=False, domain=copy.deepcopy(sortedData[3])))
	cw.addWord((3,0,1), Word(startLoc=(3,0), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addWord((4,0,1), Word(startLoc=(4,0), length=4, domain=copy.deepcopy(sortedData[4])))
	cw.addEmptyWordLocation((0,1,0))
	cw.addEmptyWordLocation((0,1,1))
	cw.addEmptyWordLocation((0,2,0))
	cw.addEmptyWordLocation((0,3,0))
	cw.addEmptyWordLocation((0,4,0))
	cw.addEmptyWordLocation((1,1,1))
	cw.addEmptyWordLocation((2,0,1))
	cw.addEmptyWordLocation((2,0,0))
	cw.addEmptyWordLocation((3,0,1))
	cw.addEmptyWordLocation((4,0,1))
	return cw

def assignWord(csp, word, assignment):
	# assign word
	word.assigned = True
	word.assignment = assignment
	word.domain = [assignment]
	
	# update grid
	for i in range(word.length):
		gridRow = word.startLoc[0]
		gridCol = word.startLoc[1]
		if word.across:	gridCol += i
		else:	gridRow += i
		csp.grid[gridRow,gridCol] = assignment[1][i]


# Constraint Propogation upon the assignment of a Word variable word
def propogateWordAssignment(csp, word):
	for i in range(word.length):
		gridRow = word.startLoc[0]
		gridCol = word.startLoc[1]
		if word.across:	gridCol += i
		else:	gridRow += i

		# Update letter domains
		letter = csp.letters[(gridRow,gridCol)]
		if letter.assigned:
			continue
		letter.domain = [word.assignment[1][i]]
		letter.assigned = True
		letter.assignment = word.assignment[1][i]

		# Update overlapping words' domains
		overlapWordKey = letter.acrossWordLoc
		overlapWordOffset = letter.acrossIdx
		if word.across:
			overlapWordKey = letter.downWordLoc
			overlapWordOffset = letter.downIdx
		overlapWord = csp.words[overlapWordKey]
		if overlapWord.assigned:
			continue

		toRemove = []
		for domWord in overlapWord.domain:
			if word.assignment[1][i] != domWord[1][overlapWordOffset]:
				toRemove.append(domWord)
		for elem in toRemove:
			overlapWord.domain.remove(elem)

def chooseSeedWord(csp, key):
	word = csp.words[key]
	random.shuffle(word.domain)
	assignWord(csp, word, word.domain[0])
	propogateWordAssignment(csp, word)
	

###------------------VARIABLE_ORDERING_ALGORITHMS------------------###

# Returns the index value of a random clue in the database
def randomClue(data):
	return random.choice(data)

# Determines Variable Ordering
def computeVariableOrderingWordByWord(csp):
	return [(0,1,1), (0,1,0), (1,1,1), (0,2,0),(2,0,1),(0,3,0),(3,0,1),(0,4,0),(4,0,1)]

def computeVariableOrderingLetterByLetter(csp):
	order = [(x,y) for x in range(csp.size) for y in range(csp.size)]
	order.remove((0,0))
	order.remove((1,0))
	order.remove((3,4))
	order.remove((4,4))
	return order

def computeVariableOrdering(csp,grid,wordByWord):
	pass

###----------------------CONSTRAINT_PROPOGATION--------------------###

def findWordFromSquare(csp, loc):
	pass

# TO FINISH
def ac3(csp, assignedWord, assignedLetter):
	# if a word variable was assigned
	if assignedWord != None:
		#for each letter in the assigned word
		for i in range(assignedWord.length):
			curLetterLoc = (assignedWord.startLoc[0]+i, assignedWord.startLoc[1])
			curLetter = assignedWord.assignment[i]
			if assignedWord.across:
				curLetterLoc = (assignedWord.startLoc[0], assignedWord.startLoc[1]+i)
			#update letter domains
			csp.letters[curLetterLoc].assigned = True
			csp.letters[curLetterLoc].assignment = curLetter
	
			#update word domains
			curWord = findWordFromSquare(csp, curLetterLoc) #unwritten function

	# if a letter variable was assigned
	else:
		pass


###----------------------------HEURISTICS--------------------------###

def rateWord(word):
	pass

###--------------------------EVALUATION---------------------------###