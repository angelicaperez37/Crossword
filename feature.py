from classes import *
from enum import Enum
import copy
from ast import literal_eval as make_tuple

#TODO: add time features, e.g. how much of the grid has been filled

### Letter types
class LetterType(Enum):
	plosive = 1
	bilibial_plosive = 2
	alveolar_plosive = 3
	velar_plosive = 4
	voiced_plosive = 5
	voiceless_plosive = 6
	fricative = 7
	nasal = 8
	approximant = 9
	vowel_consonants = 10
	uncategorized = 11
	vowel = 12
	consonant = 13
	most_common_singles = 14
	second_most_common_singles = 15
	third_most_common_singles = 16

# to indicate which letter type features we want to use
activeLetterTypeFeatures = range(1,3) +[12,13]
activeDiagonalLetterTypeFeatures = range(1,4) + [12,13]
activeAdjacentLetterTypeFeatures = range(1,5)+[12,13]

### Word Attribute Types
class WordAttribute(Enum):
	word_length = 1
	edge_word = 2
	ratio_assigned = 3
	ratio_assigned_vowels =4

activeWordAttributeFeatures = range(1,5)

### Location Features wrt Grid
class GridLocationAttribute(Enum):
	regional = 1
	index = 2
	edge_letter = 3
	double_edge_letter = 4

activeGridLocationAttributeFeatures = [3,4]

### Location Features wrt Words
class WordLocationAttribute(Enum):
	which_third = 1 #[1,2,3]
	which_half = 2 #[1,2]
	letter_idx =3

activeWordLocationAttributeFeatures = [3]

PLOSIVE = set(['P','B','T','D','K','G'])
BILIBIAL_PLOSIVE = set(['P','B'])
ALVEOLAR_PLOSIVE = set(['T','D'])
VELAR_PLOSIVE = set(['K','G'])
VOICED_PLOSIVE = set(['B','D','G'])
VOICELESS_PLOSIVE = set(['P','T','K'])
FRICATIVE = set(['F','V','S','Z','H'])
NASAL = set(['N','M'])
APPROXIMANT = set(['R'])
VOWEL_CONSONANTS = set(['J','W'])
UNCATEGORIZED = set(['C','L','Q','X','Y'])
VOWEL = set(['A','E','I','O','U'])
# CONSONANT - use VOWEL to check for consonants
MOST_COMMON_SINGLES = set(['E','T','A','O'])
SECOND_MOST_COMMON_SINGLES = set(['I','N','S','H'])
THIRD_MOST_COMMON_SINGLES = set(['D','L','U'])

class CSPFeatureExtractor():

	def extract(self, csp, cw, action, assignment):
		# feature: (name, value(normTotal/bool))
		features = []

		# Possible Word Features
		features += self.wordByWordFeatures(csp, cw, action, assignment)

		''' # Possible Letter Features
		features += self.letterTypeFeatures(assignment, '', activeLetterTypeFeatures)
		features += self.diagonalLetterFeatures(cw.blanks, csp, action)
		features += self.adjacentLetterFeatures(cw.blanks, csp, action)
		features += self.wordAttributeFeatures(cw, csp, action)
		#features += self.gridLocationAttributeFeatures(cw, csp, action)
		'''
		return features

	### Word by word Approach features
	def wordByWordFeatures(self, csp, cw, action, assignment):

		features = []
		wordLength = action.length
		# word length
		features.append(('word_length', wordLength*1.0/cw.size))

		# vowel ratio, and 3 most comman single (mcs) categories
		numVowels = 0
		numMCS = 0
		numMCS2 = 0
		numMCS3 = 0
		for ch in assignment:
			if ch in VOWEL:
				numVowels += 1
			if ch in MOST_COMMON_SINGLES:
				numMCS += 1
			if ch in SECOND_MOST_COMMON_SINGLES:
				numMCS2 += 1
			if ch in THIRD_MOST_COMMON_SINGLES:
				numMCS3 += 1
		vowelRatio = numVowels*1.0/wordLength
		mcsRatio1 = numMCS*1.0/wordLength
		mcsRatio2 = numMCS2*1.0/wordLength
		mcsRatio3 = numMCS3*1.0/wordLength
		features.append(('vowel_ratio', vowelRatio))
		features.append(('mcs1', mcsRatio1))
		features.append(('mcs2', mcsRatio2))
		features.append(('mcs3', mcsRatio3))

		# ratio of contained Letter variables assigned
		startRow = action.startLoc[0]
		startCol = action.startLoc[1]
		numAssigned = 1
		for idx in range(wordLength):
			curLetterKey = None
			if action.across:
				curLetterKey = str((startRow, startCol+idx))
			else:
				curLetterKey = str((startRow+idx, startCol))
			if len(csp.values[curLetterKey]) == 1:
				numAssigned += 1
		assignedRatio = numAssigned*1.0/wordLength
		features.append(('assigned_ratio', assignedRatio))

		return features

	### Letter type features
	def letterTypeFeatures(self, letter, prefix, activeFeatures):
		features = []

		# Letter Identity feature
		#features.append(('letter_type: ' + letter, ?))

		if 1 in activeFeatures and letter in PLOSIVE:
			features.append((prefix+'plosive', 1))
		elif 1 in activeFeatures:
			features.append((prefix+'plosive', 0))

		if 2 in activeFeatures and letter in BILIBIAL_PLOSIVE:
			features.append((prefix+'bilibial_plosive', 1))
		elif 2 in activeFeatures:
			features.append((prefix+'bilibial_plosive', 0))

		if 3 in activeFeatures and letter in ALVEOLAR_PLOSIVE:
			features.append((prefix+'alveolar_plosive', 1))
		elif 3 in activeFeatures:
			features.append((prefix+'alveolar_plosive', 0))

		if 4 in activeFeatures and letter in VELAR_PLOSIVE:
			features.append((prefix+'velar_plosive', 1))
		elif 4 in activeFeatures:
			features.append((prefix+'velar_plosive', 0))

		if 5 in activeFeatures and letter in VOICED_PLOSIVE:
			features.append((prefix+'voiced_plosive', 1))
		elif 5 in activeFeatures:
			features.append((prefix+'voiced_plosive', 0))

		if 6 in activeFeatures and letter in VOICELESS_PLOSIVE:
			features.append((prefix+'voiceless_plosive', 1))
		elif 6 in activeFeatures:
			features.append((prefix+'voiceless_plosive', 0))

		if 7 in activeFeatures and letter in FRICATIVE:
			features.append((prefix+'fricative', 1))
		elif 7 in activeFeatures:
			features.append((prefix+'fricative', 0))

		if 8 in activeFeatures and letter in NASAL:
			features.append((prefix+'nasal', 1))
		elif 8 in activeFeatures:
			features.append((prefix+'nasal', 0))

		if 9 in activeFeatures and letter in APPROXIMANT:
			features.append((prefix+'approximant', 1))
		elif 9 in activeFeatures:
			features.append((prefix+'approximant', 0))

		if 10 in activeFeatures and letter in VOWEL_CONSONANTS:
			features.append((prefix+'vowel_consonants', 1))
		elif 10 in activeFeatures:
			features.append((prefix+'vowel_consonants', 0))

		if 11 in activeFeatures and letter in UNCATEGORIZED:
			features.append((prefix+'uncategorized', 1))
		elif 11 in activeFeatures:
			features.append((prefix+'uncategorized', 0))

		if 12 in activeFeatures and letter in VOWEL:
			features.append((prefix+'vowel', 1))
		elif 12 in activeFeatures:
			features.append((prefix+'vowel', 0))

		if 13 in activeFeatures and letter in VOWEL or letter == '*':
			features.append((prefix+'consonant', 0))
		elif 13 in activeFeatures:
			features.append((prefix+'consonant', 1))

		if 14 in activeFeatures and letter in MOST_COMMON_SINGLES:
			features.append((prefix+'most_common_singles', 1))
		elif 14 in activeFeatures:
			features.append((prefix+'most_common_singles', 0))

		if 15 in activeFeatures and letter in SECOND_MOST_COMMON_SINGLES:
			features.append((prefix+'second_most_common_singles', 1))
		elif 15 in activeFeatures:
			features.append((prefix+'second_most_common_singles', 0))

		if 16 in activeFeatures and letter in THIRD_MOST_COMMON_SINGLES:
			features.append((prefix+'third_most_common_singles', 1))
		elif 16 in activeFeatures:
			features.append((prefix+'third_most_common_singles', 0))

		return features

	### Neighboring Variables Features
	# diagonal
	def diagonalLetterFeatures(self, blanks, csp, letter):
		diagonalLetterIdxs = [(letter.loc[0]-1, letter.loc[1]-1), (letter.loc[0]-1, letter.loc[1]+1), (letter.loc[0]+1, letter.loc[1]-1), (letter.loc[0]+1, letter.loc[1]+1)]
		features = []
		for i,idx in enumerate(diagonalLetterIdxs):
			dlAssignment = '*'
			letterKey = str(idx)
			if letterKey in csp.variables:
				#diagonalLetter = cw.letters[idx]
				domain = csp.values[letterKey]
				if len(domain) == 1:
					dlAssignment = domain[0]
					features.append(('diagonal_assigned_'+str(i), 1))
				else:
					features.append(('diagonal_assigned_'+str(i), 0))
			else:	features.append(('diagonal_assigned_'+str(i), 0))

			if idx in blanks:
				features.append(('diagonal_blank_'+str(i), 1))
			else:
				features.append(('diagonal_blank_'+str(i), 0))

			features += self.letterTypeFeatures(dlAssignment, 'diagonal_'+str(i)+'_', activeDiagonalLetterTypeFeatures)
		return features


	# returns adjacent letter type features
	def adjacentLetterFeatures(self, blanks, csp, letter):
		adjacentLetterIdxs = [(letter.loc[0]-1, letter.loc[1]), (letter.loc[0], letter.loc[1]+1), (letter.loc[0]+1, letter.loc[1]), (letter.loc[0], letter.loc[1]-1)]
		features = []
		for i,idx in enumerate(adjacentLetterIdxs):
			alAssignment = '*'
			letterKey = str(idx)
			if letterKey in csp.variables:
				domain = csp.values[letterKey]
				if len(domain) == 1:
					alAssignment = domain[0]
					features.append(('adjacent_assigned_'+str(i), 1))
				else:
					features.append(('adjacent_assigned_'+str(i), 0))
			else:
				features.append(('adjacent_assigned_'+str(i), 0))

			if idx in blanks:
				features.append(('adjacent_blank_'+str(i), 1))
			else:
				features.append(('adjacent_blank_'+str(i), 0))

			features += self.letterTypeFeatures(alAssignment, 'adjacent_'+str(i)+'_', activeAdjacentLetterTypeFeatures)
		return features

	### Member Word Attribute Features
	def wordAttributeFeatures(self, cw, csp, letter):
		features = []
		acrossWordLoc = letter.acrossWordLoc
		acrossWord = cw.words[acrossWordLoc]
		acrossIdx = letter.acrossIdx
		downWordLoc = letter.downWordLoc
		downWord = cw.words[downWordLoc]
		downIdx = letter.downIdx

		# word_length
		if 1 in activeWordAttributeFeatures:
			features.append(('across_word_length', acrossWord.length*1.0/cw.size))
			features.append(('down_word_length', downWord.length*1.0/cw.size))

		# edge_word
		if 2 in activeWordAttributeFeatures:
			if acrossWordLoc[0] == 0 or acrossWordLoc[0] == cw.size-1:
				features.append(('across_edge_word', 1))
			else:
				features.append(('across_edge_word', 0))
			if downWordLoc[1] == 0 or downWordLoc[1] == cw.size-1:
				features.append(('down_edge_word', 1))
			else:
				features.append(('down_edge_word', 0))

		# ratio_assigned
		if 3 in activeWordAttributeFeatures:
			assigned = 0
			for i in range(acrossWord.length):
				curLetter = cw.letters[(acrossWord.startLoc[0], acrossWord.startLoc[1]+i)]
				if len(csp.values[str(curLetter.loc)]) == 1:
					assigned += 1
			features.append(('across_ratio_assigned', assigned*1.0/acrossWord.length))
			assigned = 0
			for i in range(downWord.length):
				curLetter = cw.letters[(downWord.startLoc[0]+i, downWord.startLoc[1])]
				if len(csp.values[str(curLetter.loc)]) == 1:
					assigned += 1
			features.append(('down_ratio_assigned', assigned*1.0/downWord.length))

		# ratioAssignedVowels
		# TODO

		return features

	### Location wrt Grid Features
	def gridLocationAttributeFeatures(self, cw, csp, letter):
		features = []

		# TODO: regional
		if 1 in activeGridLocationAttributeFeatures:
			pass

		# TODO: index
		if 2 in activeGridLocationAttributeFeatures:
			pass

		blankLocations = [(x,y) for x in range(cw.size) for y in [-1,cw.size]]
		blankLocations += [(x,y) for x in [-1,cw.size] for y in range(cw.size)]
		blankLocations += copy.deepcopy(cw.blanks)

		row,col = letter.loc
		nbrs = [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]

		# edgeLetter
		if 3 in activeGridLocationAttributeFeatures:
			notEdge = True
			for n in nbrs:
				if n in blankLocations:
					features.append(('edge_letter', 1))
					notEdge = False
					break
			if notEdge:
				features.append(('edge_letter', 0))

		# doubleEdgeLetter
		if 4 in activeGridLocationAttributeFeatures:
			edges = 0
			for n in nbrs[0:2]:
				if n in blankLocations:
					edges += 1
					continue
			for n in nbrs[2:4]:
				if n in blankLocations:
					edges += 1
					continue
			if edges == 2:
				features.append(('double_edge_letter', 1))
			else:
				features.append(('double_edge_letter', 0))

		return features

	### Location wrt Word Features
	def wordLocationAttributeFeatures(self, cw, csp, letter):
		features = []

		# whichThird [1,2,3]
		if 1 in activeWordLocationAttributeFeatures:
			pass

		# whichHalf [1,2]
		if 2 in activeWordLocationAttributeFeatures:
			pass

		# letterIdx
		if 3 in activeWordLocationAttributeFeatures:
			features.append(('across_letter_idx', letter.acrossIdx*1.0/letter.acrossWord.length))
			features.append(('down_letter_idx', letter.downIdx*1.0/letter.downWord.length))

		return features
