"""The Pytris game, in all its glory.

This is where the game initialization and loop are held, and is the ultimate\n
controller of everything that goes on inside the game.
"""

import pygame
import globvars
import background
import tetramino
import sys
import copy

def MainLoop():
	"""Main pytris game loop and event parser."""
pygame.init()
playing = False
mainScreen = pygame.display.set_mode(globvars.screenSize)
pygame.display.set_caption("Pytris v%s" % globvars.versionString)
pygame.display.set_icon(pygame.image.load("icon.bmp"))
splashScreen = pygame.image.load("splash.bmp")
splashCoordinates = ((globvars.screenSize[0] / 2) - (splashScreen.get_size()[0]\
/ 2), (globvars.screenSize[1] / 2) - (splashScreen.get_size()[1] / 2))
textFont = pygame.font.Font("VeraMono.ttf", 12)
pygame.key.set_repeat(100, 100)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
			if playing:
				if event.key == pygame.K_UP:
					currTetramino.rotate()
				elif event.key == pygame.K_LEFT:
					currTetramino.shift("Left")
				elif event.key == pygame.K_RIGHT:
					currTetramino.shift("Right")
				elif event.key == pygame.K_DOWN:
					currTetramino.shift()
			else:
				playing = True
				currTetramino = tetramino.RandomTetramino()
				nextTetramino = tetramino.RandomTetramino()
				intrvl = 500 - 10 * globvars.scoreLevel
				if intrvl <= 0:
					sys.exit()
				pygame.time.set_timer(pygame.USEREVENT, intrvl)
		elif event.type == pygame.USEREVENT and playing:
			if not currTetramino.shift():
				currTetramino.freeze()
				currTetramino = copy.deepcopy(nextTetramino)
				nextTetramino = tetramino.RandomTetramino()
				if not currTetramino.check():
					sys.exit()
	if playing:
		background.DrawBackground(mainScreen)
		background.DrawBlocks(mainScreen)
		background.DrawInformation(mainScreen, textFont)
		currTetramino.draw(mainScreen)
		nextTetramino.minidraw(mainScreen, (10, 520))
	else:
		mainScreen.blit(splashScreen, splashCoordinates)
	pygame.display.flip()
	if globvars.scoreNext >= globvars.scoreNextMax:
		globvars.scoreNext = 0
		globvars.scoreLevel += 1
