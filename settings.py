from PIL import Image

#CONSTANTS

STOP_AT_UNKNOWN_CELL = True

#Board Types
BEGINNER_BOARD = (9, 9)
BEGINNER_MINES = 10

HARD_BOARD = (16, 16)
HARD_MINES = 40

EXPERT_BOARD = (30, 30)
EXPERT_MINES = 99

#Cell Types
CELL_MINE = -1
CELL_COVERED = -2
CELL_FALSE_MINE = -3
CELL_EXPLOADED_MINE = -4

#Statuses
ALIVE = 0
DEAD = 1
WIN = 2


class minesweeperGame():

    def __init__(self, field_color, tile_samples):
         # Color used to find a grid. This should be the most central color
        # of a closed cell (or several colors if it is a chess-board-like,
        # as Google Minesweeper is)
        self.field_color = field_color

        # Load sample pictures of cells
        self.samples = [(Image.open(file), value)
                        for file, value in tile_samples.items()]
        
        self.sample_sensitivity = 3000

        self.cell_padding = 1

        self.click_pause = 0.05

MINESWEEPER_MACOS = minesweeperGame(
    field_color=(95, 95, 95, 255),
    tile_samples={
        "./tiles/mac-0.png" : 0,
        "./tiles/mac-1.png" : 1,
        "./tiles/mac-2.png" : 2,
        "./tiles/mac-3.png" : 3,
        "./tiles/mac-4.png" : 4,
        "./tiles/mac-5.png" : 5,
        "./tiles/mac-6.png" : 6,
        "./tiles/mac-7.png" : 7,
        "./tiles/mac-8.png" : 8,
        "./tiles/mac-mine.png" : CELL_MINE,
        "./tiles/mac-covered.png" : CELL_COVERED,
        "./tiles/mac-FLAG.png" : CELL_MINE,
        "./tiles/mac-explosion.png" : CELL_EXPLOADED_MINE,
        }
    )