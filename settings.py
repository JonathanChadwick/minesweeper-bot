from PIL import Image
import pyscreeze

#CONSTANTS

STOP_AT_UNKNOWN_CELL = True

MINIMUM_CELL_SIZE = 10

#Board Types
BEGINNER_BOARD = (9, 9)

HARD_BOARD = (16, 16)

EXPERT_BOARD = (30, 16)

MINE_COUNTS = {
    BEGINNER_BOARD: 10,
    HARD_BOARD: 40,
    EXPERT_BOARD: 99
}

#Cell Types
CELL_MINE = -1
CELL_COVERED = 0
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

    def is_field_color(self, pixel):
        i = 0
        while i < len(self.field_color) - 1:
            if pixel[i] <= self.field_color[i] + 1 and pixel[i] >= self.field_color[1] - 1:
                i += 1
            else:
                return False
        if pixel[3] == self.field_color[3]:
            return True
        return False

MINESWEEPER_MACOS = minesweeperGame(
    field_color=(95, 95, 95, 255),
    tile_samples={
        "./tiles/empty.png" : -2,
        "./tiles/1.png" : 1,
        "./tiles/1-edge.png" : 1,
        "./tiles/1-upper-corner.png" : 1,
        "./tiles/2.png" : 2,
        "./tiles/3.png" : 3,
        "./tiles/4.png" : 4,
        "./tiles/5.png" : 5,
        # "./tiles/mac-6.png" : 6,
        # "./tiles/mac-7.png" : 7,
        # "./tiles/mac-8.png" : 8,
        "./tiles/mine.png" : CELL_EXPLOADED_MINE,
        "./tiles/covered.png" : CELL_COVERED,
        "./tiles/flag.png" : CELL_MINE,
        # "./tiles/mac-explosion.png" : CELL_EXPLOADED_MINE,
        }
    )

class ScreenProps:

    def __init__(self):

        screen = pyscreeze.screenshot()
        self.height = screen.size[1]
        self.width = screen.size[0]

SCREEN = ScreenProps()