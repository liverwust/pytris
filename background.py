"""Represents the background screen in Pytris.

Exported functions:
DrawBackground - Draw the background screen on 'surface.'
DrawBlocks - Draw all of the blocks that have already reached the bottom of the
playing field.
DrawInformation - Draw the various information displayed in the borders.
"""


import globvars
import pygame
import copy


def DrawBackground(surface):
	"""The real meat of the background module; draws the background screen.

	Keyword arguments:
	surface -- The Surface where the background screen will be drawn.

	"""
	surface.fill(globvars.colorBackground)
	surface.fill(globvars.colorMidground, pygame.Rect( \
	globvars.screenBorder, 0, globvars.screenSize[0] - ( \
	globvars.screenBorder * 2), globvars.screenSize[1]))
	pygame.draw.line(surface, globvars.colorGroundLine, ( \
	globvars.screenBorder - 2, 0), (globvars.screenBorder - 2, \
	globvars.screenSize[1]), 3)
	pygame.draw.line(surface, globvars.colorGroundLine, ( \
	globvars.screenSize[0] - globvars.screenBorder + 1, 0), ( \
	globvars.screenSize[0] - globvars.screenBorder + 1, \
	globvars.screenSize[1]), 3)
	return None

def DrawBlocks(surface):
	"""Draw the blocks already present on the playing field.

	This function also checks to see if a row is filled, and if so, adds to
	the player's score.

	Keyword arguments:
	surface -- The Surface where the blocks are to be drawn.

	"""
	blank = [False for q in range(10)]
	filled = [True for q in range(10)]
	blockY = 19
	mask = globvars.blockMask
	mask.reverse()
	blocksize = globvars.blockSize
	tmask = []
	while len(mask):
		row = mask.pop()
		if row == filled:
			mask.insert(0, blank[:])
			globvars.scoreCounter += 100 * globvars.scoreLevel
			globvars.scoreNext += 100
			continue
		tmask.append(row)
		blockX = 0
		for col in row:
			if col:
				rect = pygame.Rect(blockX * blocksize + \
				globvars.screenBorder, blockY * blocksize, \
				blocksize, blocksize)
				surface.fill(globvars.colorBlockFrozen, rect)
				pygame.draw.rect(surface, \
				globvars.colorBlockBorder, rect, 1)
			blockX += 1
		blockY -= 1
	globvars.blockMask = tmask

def DrawInformation(surface, font):
	"""Draw all of the information displayed in the screen border.

	This function is responsible for displaying things like the score and
	current level.

	Keyword arguments:
	surface - Surface upon which to draw the information.
	font - Font to be used to draw the information.
	"""
	font.set_bold(True)
	text = font.render("Score:", True, globvars.colorForeground, \
	globvars.colorBackground)
	surface.blit(text, pygame.Rect(10, 10, 0, 0))
	text = font.render("Level:", True, globvars.colorForeground, \
	globvars.colorBackground)
	surface.blit(text, pygame.Rect(410, 10, 0, 0))
	font.set_bold(False)
	text = font.render(str(globvars.scoreCounter).rjust(8, "0"), True, \
	globvars.colorForeground, globvars.colorBackground)
	surface.blit(text, pygame.Rect(10, 25, 0, 0))
	text = font.render(str(globvars.scoreLevel), True, \
	globvars.colorForeground, globvars.colorBackground)
	surface.blit(text, pygame.Rect(410, 25, 0, 0))
	text = font.render("Pytris v%s" % globvars.versionString, True, \
	globvars.colorForeground, globvars.colorBackground)
	surface.blit(text, pygame.Rect(405, 550, 0, 0))
