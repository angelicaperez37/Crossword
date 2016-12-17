from util import *
from classes import *
from feature import *
import random
import timeit
import string
from random import shuffle
from ast import literal_eval as make_tuple

class BacktrackingSearch(object):
	def __init__(self):
		# Keep track of the best assignment and weight found
		self.optimalAssignment = {}
		self.optimalWeight = 0

		# Keep track of the number of optimal assignments
		# Values should be equal for an unweighted CSP
		self.numOptimalAssignments = 0
		self.numAssignments = 0

		# Keep track of the number of times backtrack() gets called.
		self.numOperations = 0

		# Keep track of the number of operations to get to the very first successful assignment
		self.firstAssignmentNumOperations = 0

		# List of all solutions found
		self.allAssignments = []

	def print_stats(self):
		"""
		Prints a message summarizing the outcome of the solver.
		"""
		if self.optimalAssignment:
			print 'Found %d optimal assignments with weight %f in %d operations' \
			% (self.numOptimalAssignments, self.optimalWeight, self.numOperations)
			print 'First assignment took %d operations' % self.firstAssignmentNumOperations
		else:
			print 'No solution was found.'

	def get_delta_weight(self, assignment, var, val):
		"""
		Given a CSP, a partial assignment, and a proposed new value for a variable,
		return the change of weights after assigning the variable with the proposed value.

		@param assignment: A dictionary of current assignment. Unassigned variables
		do not have entries, while an assigned variable has the assigned value
		as a value in dictionary. e.g. if the domain of the variable A is [5,6],
		and 6 was assigned to it, then assignment[A] == 6.

		@param var: name of an unassigned variable.
		@param val: the proposed value.

		@return w: Change in weights as a result of the proposed assignment.
		This will be used as a multiplier on the current weight.
		"""
		assert var not in assignment
		w = 1.0
		if self.csp.unaryFactors[var]:
			w *= self.csp.unaryFactors[var][val]
			if w == 0:	return w
		for var2, factor in self.csp.binaryFactors[var].iteritems():
			if var2 not in assignment:	continue
			w *= factor[val][assignment[var2]]
			if w == 0:	return w
		return w

	def get_score_test(self, assignment, var, val, weights):
		if len(make_tuple(var)) > 2:	return self.get_delta_weight(assignment, var, val)
		w = weights[string.ascii_uppercase.index(val)]
		fv = self.featureExtractor.extract(self.csp, self.cw, self.cw.letters[make_tuple(var)], val)
		fv_vals = [feat[1] for feat in fv]
		vec = np.multiply(w, fv_vals)
		return np.linalg.norm(vec)

	def get_score(self, assignment, var, val):

		tempDomains = {}
		for key in self.domains.keys():
			tempDomains[key] = copy.deepcopy(self.domains[key])
		tempDomains[var] = [val]

		# score based on magnitudes of domains after propogation
		cumulativeScore = 0.0
		totalSamples = 0
		q = []
		checked = []
		q.append(var)
		while(len(q) > 0):
			curVar = q.pop(0)
			checked.append(curVar)
			domainCurVar = tempDomains[curVar]
			if len(domainCurVar) == 0:
					continue

			# Iterate through neighbors(overlapping Letter/Word vars) of curVar
			for var2 in self.csp.get_neighbor_vars(curVar):
				totalDomain = 0
				numValidDomain = 0
				domainVar2 = tempDomains[var2]

				#print 'Comparing '+str(var)+ ' to '+str(var2)+'.'
				#print str(var2) + ' has domain of size ' + str(len(domainVar2))

				for b in domainVar2:


					bPossible = 0
					#if self.csp.binaryFactors[curVar][var2] is not None:
					for a in domainCurVar:

						#print 'Var1 val: '+str(a)
						#print 'Var2 val: '+str(b)

						if self.csp.binaryFactors[curVar][var2][a][b] > 0:
							bPossible = 1
							break

					totalDomain += 1
					if bPossible != 0:
						numValidDomain += 1
					else:
						domainVar2.remove(b)

				#print 'totalDomain size: '+ str(totalDomain )

				#print 'Found ' + str(numValidDomain) + ' valid values out of ' + str(totalDomain)

				if var2 not in checked and var2 not in q:
					q.append(var2)
				if totalDomain > 0:
					cumulativeScore += numValidDomain*1.0/totalDomain

					#print 'Added sample with score of ' + str(numValidDomain*1.0/totalDomain)

					totalSamples += 1
				if totalSamples == 0:	return cumulativeScore
		return cumulativeScore / totalSamples

	def solve(self, cw, csp, mcv = False, ac3 = False):
		"""
		Solves the given weighted CSP using heuristics as specified in the
		parameter. Note that unlike a typical unweighted CSP where the search
		terminates when on solution is found, we want this function to find
		all possible assignments. The results are stored in the variables
		described in reset_result().

		@param csp: A weighted CSP.
		@param mcv: When enabled, Most Constrained Variable heuristics
		is used.
		@param ac3: When enabled, AC-3 will be used after each assignment
		of a variable made.
		"""

		self.cw = cw
		self.csp = csp
		self.mcv = mcv
		self.ac3 = ac3
		self.reason = 'No reason.'
		self.explorationProb = 0.2
		self.featureVectors = {}
		self.domainPercentages = {}
		self.assignments = {}
		self.featureExtractor = CSPFeatureExtractor()
		#self.reset_results()
		self.domains = {var: list(self.csp.values[var]) for var in self.csp.variables}
		solution = self.backtrack_wbw({}, 0,1)
		return (solution, self.featureVectors, self.domainPercentages, self.assignments, self.reason)
		#self.print_stats()

	def solve_test(self, weights, cw, csp, mcv = False, ac3 = False):
		self.cw = cw
		self.csp = csp
		self.mcv = mcv
		self.ac3 = ac3
		self.featureExtractor = CSPFeatureExtractor()
		self.weights = weights
		#self.reset_results()
		self.domains = {var: list(self.csp.values[var]) for var in self.csp.variables}

		# add seed word to ensure variety
		seedVar = None
		for var in self.csp.variables:
			if len(make_tuple(var)) > 2:
				seedVar = var
				break
		seedAssignment = self.domains[seedVar][random.randint(0,len(self.domains[seedVar])-1)]
		self.domains[seedVar] = [seedAssignment]
		self.csp.values[seedVar] = [seedAssignment]
		varsAssigned = self.arc_consistency_check(seedVar)

		solution = self.backtrack_test({seedVar: seedAssignment}, 1, weights)
		return solution

	def backtrack_test(self, assignment, numAssigned, weights):
		self.numOperations += 1
		if numAssigned == self.csp.numVars: # or 0 in domainSizes:
			# Solution found
			self.numAssignments += 1
			newAssignment = {}
			for var in self.csp.variables:
				newAssignment[var] = assignment[var]
			return newAssignment

		# Select next variable to be assigned
		var = self.get_unassigned_variable(assignment)
		if var == None:
			return copy.deepcopy(assignment)

		# Get an ordering of the values.
		shuffle(self.domains[var])
		ordered_values = self.domains[var]

		# Continue the backtracking recursion using |var| and |ordered_values|
		if not self.ac3:
			for val in ordered_values:
				deltaWeight = self.get_score(assignment, var, val)
				if deltaWeight > 0:
					assignment[var] = val

					newAssignment = self.backtrack_test(assignment, numAssigned+1, weight*deltaWeight)
					del assignment[var]
					return newAssignment
		else:
			# apply heuristic to choose best assignment
			# and store features for all possible assignments
			maxScore = float('-inf')
			maxVal = None
			varKeyTup = make_tuple(var)
			for i,val in enumerate(ordered_values):
				# only check first five random
				#print 'Computing score for variable ' + str(var) + 'on assignment '+val
				score = self.get_score_test(assignment, var, val, weights)

				if score > maxScore:
					maxScore = score
					maxVal = val

				#print 'score for '+str(val)+': '+str(score)
				#print 'maxScore: ' + str(maxScore)

			# Choose assignment w/ max score
			assignment[var] = maxVal
			#localCopy = copy.deepcopy(self.domains)
			self.domains[var] = [maxVal]
			self.csp.values[var] = [maxVal]
			varsAssigned = self.arc_consistency_check(var)
			solution = self.backtrack_test(assignment, numAssigned+varsAssigned+1, weights)

			#self.domains = localCopy
			#del assignment[var]
			return solution
		# if no assignment found for variable
		return copy.deepcopy(assignment)

	def backtrack_wbw(self, assignment, numAssigned, weight):
		"""
		Perform the back-tracking algorithm to find a solution to the CSP.

		@param assignment: A dictionary of current assignments. Unassigned
		variables do not have entries, while an assigned variable has the
		assigned value as value in the dictionary. e.g. if the domain of the
		variable A is [5,6], and 6 was assigned to it, then
		assignment[A] == 6.

		@param numAssigned: Number of currently assigned variables
		@param weight: The weight of the current partial assignment.
		"""

		self.numOperations += 1
		if numAssigned == self.csp.numVars: # or 0 in domainSizes:
			# Solution found
			self.numAssignments += 1
			newAssignment = {}
			for var in self.csp.variables:
				newAssignment[var] = assignment[var]

			self.reason = 'Solved.'

			return newAssignment

		# Select next variable to be assigned
		var = self.get_unassigned_variable_wbw(assignment)

		if var == None:
			self.reason = 'No more Word variables with unempty domains.'
			return copy.deepcopy(assignment)

		# Get a random ordering of the values.
		shuffle(self.domains[var])
		ordered_values = self.domains[var]

		# Continue the backtracking recursion using |var| and |ordered_values|
		if not self.ac3:
			for val in ordered_values:
				deltaWeight = self.get_score(assignment, var, val)
				if deltaWeight > 0:
					assignment[var] = val

					newAssignment = self.backtrack_wbw(assignment, numAssigned+1, weight*deltaWeight)
					del assignment[var]
					return newAssignment
		else:
			# apply heuristic to choose best assignment
			# and store features for all possible assignments
			maxScore = -1.0
			maxVal = None
			scores = {}
			fvInstance = {}
			varKeyTup = make_tuple(var)
			for i,val in enumerate(ordered_values):
				# only check first five random
				#print 'Computing score for variable ' + str(var) + 'on assignment '+val
				score = self.get_delta_weight(assignment, var, val)
				scores[val] = score
				#print score
				if score > maxScore:
					maxScore = score
					maxVal = val

				# keep track of features
				if len(varKeyTup) > 2:
					fvInstance[val] = self.featureExtractor.extract(self.csp, self.cw, self.cw.words[varKeyTup], maxVal)
			if random.random() < self.explorationProb and len(varKeyTup) > 2:# or maxVal == None:
				foundValue = False
				for v in ordered_values:
					if scores[v] > 0:
						maxVal = v
						maxScore = scores[maxVal]
						foundValue = True
						break
				if not foundValue:
					self.reason = 'Hit dead end.'
					return copy.deepcopy(assignment)

			# stores all feature vectors for all assignments and all variables
			# fvInstance holds feature vecs for this instance
			if len(varKeyTup) > 2:
				self.featureVectors[numAssigned] = fvInstance
				self.domainPercentages[numAssigned] = maxScore
				self.assignments[numAssigned] = maxVal
				#print 'HERE' + str(varKeyTup) + '\n'


			# Choose assignment w/ max score
			assignment[var] = maxVal
			#localCopy = copy.deepcopy(self.domains)
			self.domains[var] = [maxVal]
			self.csp.values[var] = [maxVal]
			addAssignmentsToGrid(self.cw, {var: maxVal})

			#print 'Assigned value '+str(maxVal) + ' to variable ' + str(var)
			#print self.cw.grid

			varsAssigned = self.arc_consistency_check(var)
			solution = self.backtrack_wbw(assignment, numAssigned+varsAssigned+1, weight)

			#self.domains = localCopy
			#del assignment[var]
			return solution
		# if no assignment found for variable
		self.reason = 'No solution found.'
		return copy.deepcopy(assignment)

	def backtrack(self, assignment, numAssigned, weight):
		"""
		Perform the back-tracking algorithm to find a solution to the CSP.

		@param assignment: A dictionary of current assignments. Unassigned
		variables do not have entries, while an assigned variable has the
		assigned value as value in the dictionary. e.g. if the domain of the
		variable A is [5,6], and 6 was assigned to it, then
		assignment[A] == 6.

		@param numAssigned: Number of currently assigned variables
		@param weight: The weight of the current partial assignment.
		"""

		self.numOperations += 1
		if numAssigned == self.csp.numVars: # or 0 in domainSizes:
			# Solution found
			self.numAssignments += 1
			newAssignment = {}
			for var in self.csp.variables:
				newAssignment[var] = assignment[var]

			self.reason = 'Solved.'

			return newAssignment

		# Select next variable to be assigned
		var = self.get_unassigned_variable(assignment)
		if var == None:
			self.reason = 'All variables have no domain left.'
			return copy.deepcopy(assignment)

		# Get an ordering of the values.
		shuffle(self.domains[var])
		ordered_values = self.domains[var]

		# Continue the backtracking recursion using |var| and |ordered_values|
		if not self.ac3:
			for val in ordered_values:
				deltaWeight = self.get_score(assignment, var, val)
				if deltaWeight > 0:
					assignment[var] = val

					newAssignment = self.backtrack(assignment, numAssigned+1, weight*deltaWeight)
					del assignment[var]
					return newAssignment
		else:
			# apply heuristic to choose best assignment
			# and store features for all possible assignments
			maxScore = -1.0
			maxVal = None
			scores = {}
			fvInstance = {}
			varKeyTup = make_tuple(var)
			for i,val in enumerate(ordered_values):
				# only check first five random
				#print 'Computing score for variable ' + str(var) + 'on assignment '+val
				score = self.get_delta_weight(assignment, var, val)
				scores[val] = score
				#print score
				if score > maxScore:
					maxScore = score
					maxVal = val

				# keep track of features
				if len(varKeyTup) == 2:
					fvInstance[val] = self.featureExtractor.extract(self.csp, self.cw, self.cw.letters[varKeyTup], maxVal)
			if random.random() < self.explorationProb and len(varKeyTup) == 2:# or maxVal == None:
				foundValue = False
				for v in ordered_values:
					if scores[v] > 0:
						maxVal = v
						maxScore = scores[maxVal]
						foundValue = True
						break
				if not foundValue:
					self.reason = 'Hit dead end.'
					return copy.deepcopy(assignment)

			# stores all feature vectors for all assignments and all variables
			# fvInstance holds feature vecs for this instance
			self.featureVectors[numAssigned] = fvInstance
			self.domainPercentages[numAssigned] = maxScore
			self.assignments[numAssigned] = maxVal
			#print 'HERE' + str(varKeyTup) + '\n'


			# Choose assignment w/ max score
			assignment[var] = maxVal
			#localCopy = copy.deepcopy(self.domains)
			self.domains[var] = [maxVal]
			self.csp.values[var] = [maxVal]
			addAssignmentsToGrid(self.cw, {var: maxVal})

			#print 'Assigned value '+str(maxVal) + ' to variable ' + str(var)
			#print self.cw.grid

			varsAssigned = self.arc_consistency_check(var)
			solution = self.backtrack(assignment, numAssigned+varsAssigned+1, weight)

			#self.domains = localCopy
			#del assignment[var]
			return solution
		# if no assignment found for variable
		self.reason = 'No solution found.'
		return copy.deepcopy(assignment)

	def get_unassigned_variable_wbw(self, assignment):
		"""
		Given a partial assignment, return a currently unassigned variable.

		@param assignment: A dictionary of current assignment.
		@return var: a currently unassigned variable
		"""
		for v in self.csp.variables:
			if len(make_tuple(v)) > 2:
				if len(self.domains[v]) > 0 and v not in assignment:
					return v
		return None


	def get_unassigned_variable(self, assignment):
		"""
		Given a partial assignment, return a currently unassigned variable.

		@param assignment: A dictionary of current assignment.
		@return var: a currently unassigned variable
		"""
		for v in self.csp.variables:
			if len(self.domains[v]) > 0 and v not in assignment:
				return v
		return None

		if not self.mcv:
			# Select a variable without any heuristicss
			for var in self.csp.variables:
				if var not in assignment:	return var
		else:
			minVals = float("inf")
			minVar = float("inf")
			for var in self.csp.variables:
				if var not in assignment.keys():
					numVals = 0
					for a in self.domains[var]:
						if self.get_delta_weight(assignment, var, a) > 0:
							numVals += 1
					if numVals < minVals:
						minVals = numVals
						minVar = var
			return minVar

	def arc_consistency_check(self, var):
		"""
		Perform the AC-3 algorithm. The goal is to reduce the size of the
		domain values for the unassigned variables based on arc consistency.

		@param var: The variable whose value has just been set.
		"""

		numAssigned = 0
		q = []
		q.append(var)
		while(len(q) > 0):
			curVar = q.pop(0)

			domainCurVar = copy.deepcopy(self.domains[curVar])
			if len(domainCurVar) == 0:
				continue

			# Iterate through neighbors(overlapping Letter/Word vars) of curVar
			for var2 in self.csp.get_neighbor_vars(curVar):

				domainVar2 = copy.deepcopy(self.domains[var2])
				for b in domainVar2:
					'''
					if self.csp.unaryFactors[var2] is not None:
						if self.csp.unaryFactors[var2][b] == 0:
							self.domains[var2].remove(b)
							if var2 not in q:
								q.append(var2)
							continue
					'''

					bPossible = 0
					#if self.csp.binaryFactors[curVar][var2] is not None:
					for a in domainCurVar:

						#print curVar
						#print var2
						#print a
						#print b

						if self.csp.binaryFactors[curVar][var2][a][b] > 0:
							bPossible = 1
							break
					if bPossible == 0:
						self.domains[var2].remove(b)
						if var2 not in q:
							q.append(var2)

		return numAssigned


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

	return True
