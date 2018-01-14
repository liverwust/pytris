"""Routines to manipulate on-screen tetraminos.

Exported classes:
Tetramino -- Logical representation of an on-screen tetramino.

Exported functions:
RandomTetramino -- Generate a randomly-shaped tetramino.
"""


import pygame
import globvars
import copy
import random


class Tetramino:

	"""The logical representation of on-screen tetraminos.

	Constructor arguments:
	shape -- The shape to be taken by the tetramino (see shapes.txt).
	
	Member functions:
	draw -- Draw the tetramino onto a given Surface.
	minidraw -- Draw a miniature version of the tetramino.
	rotate -- Rotate the tetramino (counter)clockwise by 90 degrees.
	check -- Check to see if a position can occupy the tetramino.
	shift -- Move the tetramino left, right, or down.
	freeze -- Freeze the tetramino and add it to the blockMask.
	"""

	def __init__(self, shape):
		"""Initialize a tetramino.

		Keyword arguments:
		shape -- Shape of the tetramino as a string (see shape.txt).
		"""
		self._position = (19, 5)
		# Generate shape matrix
		if shape == "I":
			self._matrix = [[True for c in range(4)]]
		elif shape == "J":
			self._matrix = [[True for c in range(3)] for r in \
			range(2)]
			self._matrix[1] = [False, False, True]
		elif shape == "L":
			self._matrix = [[True for c in range(3)] for r in \
			range(2)]
			self._matrix[1] = [True, False, False]
		elif shape == "O":
			self._matrix = [[True for c in range(2)] for r in \
			range(2)]
		elif shape == "S":
			self._matrix = [[True for c in range(3)] for r in \
			range(2)]
			self._matrix[0] = [False, True, True]
			self._matrix[1] = [True, True, False]
		elif shape == "T":
			self._matrix = [[True for c in range(3)] for r in \
			range(2)]
			self._matrix[1] = [False, True, False]
		elif shape == "Z":
			self._matrix = [[True for c in range(3)] for r in \
			range(2)]
			self._matrix[0] = [True, True, False]
			self._matrix[1] = [False, True, True]
		else:
			raise ValueError("bad tetramino shape %s" % shape)

	def draw(self, surface):
		"""Draw this tetramino on a pygame Surface.

		Keyword arguments:
		surface -- The pygame Surface to draw the tetramino upon.
		"""
		baseX = self._position[1] * globvars.blockSize
		baseY = (19 - self._position[0]) * globvars.blockSize
		posY = baseY
		for row in self._matrix:
			posX = baseX
			for col in row:
				if col:
					rect = pygame.Rect(posX + \
					globvars.screenBorder, posY, \
					globvars.blockSize, globvars.blockSize)
					surface.fill(globvars.colorBlockActive,\
					rect)
					pygame.draw.rect(surface, \
					globvars.colorBlockBorder, rect, 1)
				posX += globvars.blockSize
			posY += globvars.blockSize

	def minidraw(self, surface, position):
		"""Draw a miniature, preview version of this tetramino.

		Keyword arguments:
		surface -- The pygame Surface to draw the tetramino upon.
		position -- The (x, y) coordinates at which to draw.
		"""
		posY = 0
		for row in self._matrix:
			posX = 0
			for col in row:
				if col:
					rect = pygame.Rect(posX + position[0], \
					posY + position[1], \
					globvars.blockSizeMini, \
					globvars.blockSizeMini)
					surface.fill(globvars.colorBlockActive,\
					rect)
					pygame.draw.rect(surface, \
					globvars.colorBlockBorder, rect, 1)
				posX += globvars.blockSizeMini
			posY += globvars.blockSizeMini
		pygame.draw.rect(surface, globvars.colorForeground, \
		pygame.Rect(position[0], position[1], 4 * \
		globvars.blockSizeMini + 5, 4 * globvars.blockSizeMini + 5), 1)

	def rotate(self, clockwise = True):
		"""Rotate this tetramino by 90 degrees.

		Keyword arguments:
		clockwise -- True: clockwise  False: counterclockwise

		Returns True if the rotation was possible, False otherwise.
		"""
		oldmatrix = self._matrix
		newmatrix = [[False for x in range(len(oldmatrix))] for y \
		in range(len(oldmatrix[0]))]
		if clockwise:
			seqX = range(len(oldmatrix) - 1, -1, -1)
			seqY = range(len(oldmatrix[0]))
		else:
			seqX = range(len(oldmatrix))
			seqY = range(len(oldmatrix[0]) - 1, -1, -1)
		nX = nY = 0
		for oX in seqX:
			nX = 0
			for oY in seqY:
				newmatrix[nX][nY] = oldmatrix[oX][oY]
				nX += 1
			nY += 1
		self._matrix = newmatrix
		if not self.check():
			self._matrix = oldmatrix
			return False
		else:
			return True

	def check(self, position = None):
		"""See if a particular position can accomodate this tetramino.

		Keyword arguments:
		position -- Tuple in (row, column) naming the position.
		If position == None (default), the current position is checked.
		
		Returns True if the position can accomodate this tetramino, or
		False otherwise.
		"""
		if position:
			(fieldY, fieldX) = position
		else:
			(fieldY, fieldX) = self._position
		outsideY = fieldY - len(self._matrix)
		outsideX = fieldX + len(self._matrix[0])
		if outsideY < -1 or outsideX > 10 or fieldY > 20 or fieldX < 0:
			return False
		maskX = fieldX
		maskY = fieldY
		for row in self._matrix:
			maskX = fieldX
			for col in row:
				if col and globvars.blockMask[maskY][maskX]:
					return False
				maskX += 1
			maskY -= 1
		return True

	def shift(self, direction = "Down", amount = 1):
		"""Move the tetramino in one direction by a given amount.

		Keyword arguments:
		direction -- Possibilities: "Left," "Right," "Down" (default).
		amount -- How many spaces to move, defaults to 1.

		Returns True if the shift is possible, False otherwise.
		"""
		newposition = list(copy.copy(self._position))
		if direction == "Down":
			newposition[0] = self._position[0] - 1
		elif direction == "Left":
			newposition[1] = self._position[1] - 1
		elif direction == "Right":
			newposition[1] = self._position[1] + 1
		else:
			raise ValueError("direction must be Left/Right/Down")
		if self.check(newposition):
			self._position = tuple(newposition)
			return True
		else:
			return False

	def freeze(self):
		"""Freeze this tetramino onto the playing field."""
		position = list(self._position)
		for row in self._matrix:
			position[1] = self._position[1]
			for col in row:
				if col:
					globvars.blockMask[position[0]]\
					[position[1]] = True
				position[1] += 1
			position[0] -= 1
		globvars.scoreCounter += 10 * globvars.scoreLevel
		globvars.scoreNext += 10


def RandomTetramino():
	"""Generate a random tetramino.

	Returns an object of the Tetramino class (see tetramino.Tetramino).
	"""
	return Tetramino({0: "I", 1: "J", 2: "L", 3: "O", 4: "S", 5: "T", 6: \
	"Z"}[random.randint(0,6)])
