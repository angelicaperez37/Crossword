import sys
import collections
from graphics import *

###------------------------CROSSWORD BUILDER------------------------###


class crosswordBuilder():

# Puzzle Construction:
#   1) Pick grid size
	def gridSize(self):
		width = 15
		length = 15
		return (width, length)

#   2) List Words/Phrases (a lot)
#   3) Sort list based on length
	#Get Words
		#theme?
		#ask for words from user
		#suggest theme words
		#sort words based on length

#   4) Place some long words on board
#       -symmetrically: either in the center, or a pair of words of same length
#       -check for traps: (i.e. ending in 'q', or 'kx' or 'iy' pairings)
#
#		-find possible anchor words combinations and present to user
#		-let user choose
#		-


#   5) Mark any required black spaces
#       -beginnings and ends of words
#   6) Arrange the rest of black spaces (diagonally symmetric)
#       -standard: 1/6 of squares are black
#       -avoid 2 and 3-letter words
#   7) Complete the Grid
#   8) Write Clues
#       -1/3: straightforward (i.e. exhausted -> tired)
#       -1/3: clever (i.e.  bamboo eaters: panda, farm animals: ants)
#       -1/3: fill-ins, names, and crosswordese
#           -crosswordese: (i.e. bizarre words)

win = GraphWin()
rect = Rectangle(Point(10, 10), Point(50,50))
rect.draw(win)
rect = Rectangle(Point(50, 10), Point(90,50))
rect.draw(win)
win.getMouse()
win.close()

