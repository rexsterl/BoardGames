"""
Xiangqi Game Constants
Defines game configuration, colors, and dimensions
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Board dimensions
SQUARE_SIZE = 60
BOARD_OFFSET_X = 150
BOARD_OFFSET_Y = 80

# Colors (RGB)
BOARD_COLOR = (245, 222, 179)  # Wheat color for traditional board
LINE_COLOR = (0, 0, 0)  # Black lines
PALACE_COLOR = (200, 150, 100)  # Darker color for palace
RIVER_COLOR = (100, 100, 150)  # Blue-ish for river text

# Piece colors
RED_PIECE_COLOR = (200, 0, 0)  # Red pieces
BLACK_PIECE_COLOR = (0, 0, 0)  # Black pieces

# Highlight colors
HIGHLIGHT_COLOR = (255, 255, 0, 128)  # Yellow with transparency
VALID_MOVE_COLOR = (0, 255, 0, 128)  # Green with transparency

# Game settings
FPS = 60

# AI settings
AI_SEARCH_DEPTH = 3  # Depth for minimax search
