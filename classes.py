###-----------------------CROSSWORD CLASS--------------------------###

import numpy as np

# CSP variables are represented as the classes Word and Letter,
# which are the blank spaces in the puzzle.
# Variable domains are stored in the Word and Letter objects.
class Crossword:
	def __init__(self, blanks, size=5):
		self.size = size
		self.blanks = blanks
		self.grid = np.chararray((size,size)) #np.matrix([[0]*size]*size)
		self.grid[:] = '*'
		self.emptyWordLocations = []
		self.emptyLetterLocations = []
		self.words = {} #keys = (a,b,c) where (a,b) is the start location anc c = 1 if across, 0 if not
		self.letters = {} #keys are grid locations

	def addWord(self, key, word):
		self.words[key] = word

	def addLetter(self, letter):
		self.letters[letter.loc] = letter

	def addEmptyWordLocation(self, key):
		self.emptyWordLocations.append(key)

	def addEmptyLetterLocation(self, key):
		self.emptyLetterLocations.append(key)

class Word:
	def __init__(self, startLoc=None, length=None, across=True, assigned=False, assignment=None, domain=None):
		self.startLoc = startLoc
		self.length = length
		self.across = across
		self.assigned = assigned
		self.assignment = assignment
		self.domain = domain

class Letter:
	def __init__(self, loc, acrossWordLoc=None, acrossIdx=None, \
	downWordLoc=None, downIdx=None, assigned=False, assignment = None, \
	domain=None):
		self.loc = loc
		self.acrossWordLoc = acrossWordLoc
		self.acrossIdx = acrossIdx
		self.downWordLoc = downWordLoc
		self.downIdx = downIdx
		self.assigned = assigned
		self.assignment = assignment
		self.domain = domain
