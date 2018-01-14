"""Various global variables for use in other modules.

Exported variables:
blockMask -- A 20x10 matrix of booleans which represents each block position.
blockSize -- The size (in pixels) of a single block in a tetrimino.
blockSizeMini -- Miniaturized block size (in pixels).
colorBackground -- The background color of the screen.
colorBlockActive -- Color of an active (falling) tetramino block.
colorBlockBorder -- Color of the border between each block.
colorBlockFrozen -- Color of a frozen (at the bottom) tetramino block.
colorGroundLine -- Color of the line between the midground and the background.
colorForeground -- Default foreground color for on-screen text.
colorMidground -- Color of the midground (the block area).
screenBorder -- Size (in pixels) around the midground.
screenSize -- Tuple representing the width and height of the window.
scoreCounter -- The player's current score.
scoreLevel -- The player's current level.
scoreNext -- Points towards the next level
scoreNextMax -- Points needed for a next level.
versionString -- Version information about Pytris.
"""


blockMask = [[False for c in range(10)] for r in range(20)]
blockSize = 30
blockSizeMini = 15
colorBackground = (0, 0, 0)
colorBlockActive = (0, 0, 255)
colorBlockBorder = (64, 64, 64)
colorBlockFrozen = (128, 128, 0)
colorForeground = (255, 255, 255)
colorGroundLine = (0, 128, 0)
colorMidground = (128, 0, 0)
screenBorder = 100
screenSize = (500, 600)
scoreCounter = 0
scoreLevel = 1
scoreNext = 0
scoreNextMax = 500
versionString = "0.5.1"
