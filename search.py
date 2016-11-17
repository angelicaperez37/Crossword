from util import *
from classes import *
import random 
import timeit

# Basic Word-by-Word Search w/ One Level of Forward Checking
#	*) For each Word variable, chooses first assignment that 
#		leads to non-empty neighbors' domains upon FC
def basicSearch(sortedData, csp, order):

	# Loop over word variables:
	for (row, col, across) in order:

		# Look for Word assignment
		word = csp.words[(row,col,across)]
		assignment = None
		random.shuffle(word.domain)
		for clue in word.domain:

			# Choose possible word
			val = clue[1]
			valid = True


			# Forward Checking kinda
			for i in range(word.length): #for each letter
				curRow = row
				curCol = col
				overlapAcross = 1
				if across:
					curCol = col+i
					overlapAcross = 0
				else:
					curRow = row+i

				# Check letter domains
				curLetter = csp.letters[(curRow,curCol)]

				if val[i] not in curLetter.domain:
					valid = False
					break

				# Check overlapping words' domains
				overlapWordKey = curLetter.acrossWordLoc
				if across:
					overlapWordKey = curLetter.downWordLoc

				overlapWord = csp.words[overlapWordKey]
				if overlapWord.assigned:
					continue
				overlapIdx = curLetter.acrossIdx
				singleLocDomain = [] # will hold all letters at the overlapIdx of each domain value of the overlapping word
				if across:
					overlapIdx = curLetter.downIdx
				for oVal in overlapWord.domain:
					singleLocDomain.append(oVal[1][overlapIdx])

				if val[i] not in singleLocDomain:
					valid = False
					break

			if not valid:
				continue
			else:
				assignment = clue
				break

		if assignment is not None:
			assignWord(csp, word, assignment)
		else:
			return False

		# Constraint Propogation
		propogateWordAssignment(csp, word)

	print csp.grid
	return True

# Basic Letter-By-Letter Search w/ Magnitude/NeighborAverage Scoring
#	*) Score = alpha*x + beta*y
#		x = total magnitude of neighbors' domains after FC
#		y = mean size of neighbors' domains after FC
def basicLetterByLetterSearch(sortedData, csp, order):

	random.shuffle(order)

	# Loop over word variables:
	for (row, col) in order:

		if csp.letters[(row,col)].assigned:
			continue

		# Look for letter to assign to current Letter variable
		letterVar = csp.letters[(row,col)]
		random.shuffle(letterVar.domain)

		maxScore = 0
		maxAssignment = None

		for letter in letterVar.domain:

			# Choose possible Letter
			val = letter

			# Forward Checking kinda
			acrossWord = csp.words[letterVar.acrossWordLoc]
			acrossIdx = letterVar.acrossIdx
			downWord = csp.words[letterVar.downWordLoc]
			downIdx = letterVar.downIdx

			# Variable to keep track of overlapping Word Variable domains sizes
			acrossDomSize = 0
			downDomSize = 0

			# Check across overlapping word
			for domWord in acrossWord.domain:
				if domWord[1][acrossIdx] == val:
					acrossDomSize += 1

			# Check down overlapping word
			for domWord in downWord.domain:
				if domWord[1][downIdx] == val:
					downDomSize += 1

			score = (acrossDomSize+downDomSize)/2.0
			if acrossDomSize == 0 or downDomSize == 0:
				continue
			elif random.uniform(0,1) > 0.7: #to keep things spicy
				continue
			elif score > maxScore:
				maxScore = score
				maxAssignment = val

		if maxAssignment is not None:
			letterVar.assigned = True
			letterVar.assignment = maxAssignment
			letterVar.domain = [maxAssignment]
			csp.grid[row, col] = letterVar.assignment
		else:
			return False

		# Constraint Propogation (Only for two overlapping Word variables)
		toRemove = []
		for domWord in acrossWord.domain: #across overlap
			if letterVar.assignment != domWord[1][acrossIdx]:
				toRemove.append(domWord)
		for elem in toRemove:
			acrossWord.domain.remove(elem)
		if len(acrossWord.domain) == 1:
			assignWord(csp, acrossWord, acrossWord.domain[0])
			propogateWordAssignment(csp, acrossWord)

		toRemove = []
		for domWord in downWord.domain: #down overlap
			if letterVar.assignment != domWord[1][downIdx]:
				toRemove.append(domWord)
		for elem in toRemove:
			downWord.domain.remove(elem)
		if len(downWord.domain) == 1:
			assignWord(csp, downWord, downWord.domain[0])
			propogateWordAssignment(csp, downWord)

	print csp.grid
	return True
