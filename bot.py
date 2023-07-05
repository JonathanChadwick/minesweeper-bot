
import pyautogui
import numpy

from settings import MINESWEEPER_MACOS
from util import find_game

class MinesweeperBot:

    def __init__(self, settings=MINESWEEPER_MACOS):
        self.board, self.board_size, self.mine_count, is_valid_game = find_game()
        if not is_valid_game:
            print("Sorry - no game found. Exiting")

    def click(self, coordinates):
        
        left, top, right, bottom = self.board[coordinates]


        #For Macs with Retna display - there are 4 pixels per mouse coordinate
        # Divide pixel by 2 to get correct mouse coordinate
        x = ((left + right) // 2) // 2
        y = ((bottom + top) // 2) // 2

        pyautogui.click(x, y)

    def read_board(self):

        board = numpy.zeros(self.board_size)
        print(board)
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                left, top, right, bottom = self.board[i, j]
                tile_image = pyautogui.screenshot()
                cropped = tile_image.crop((left, top, right, bottom))
                filename = f"./tiles/unknown{i}-{j}.png"
                cropped.save(filename)
                

game = MinesweeperBot()

#once to bring into focus
game.click((0, 0))

game.click((0, 0))
game.read_board()




