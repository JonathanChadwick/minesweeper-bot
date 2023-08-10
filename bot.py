
import random
import threading
import pyautogui
import numpy
from pynput.keyboard import Key, Listener

from settings import CELL_EXPLOADED_MINE, CELL_MINE, MINESWEEPER_MACOS
from util import find_game, identify_tile

class MinesweeperBot:

    def __init__(self, settings=MINESWEEPER_MACOS):
        self.board, self.board_size, self.mine_count, is_valid_game = find_game()

        self.game_state = numpy.zeros(self.board_size)

        self.mines = set([])

        self.status = "playing"
        if not is_valid_game:
            print("Sorry - no game found. Exiting")
            return
    
    def keyboard_listener(self):
        def on_press(key):
            pass

        def on_release(key):
            print('{0} release'.format(
            key))
            if key== Key.f5:
                with open("debug.txt", "w") as f:
                    f.write(numpy.array2string(self.game_state))
            if key == Key.esc:
                # Stop listener
                return False
            
        # Collect events until released
        listener = Listener(on_press=on_press, on_release=on_release)
        thread = threading.Thread(target=listener.start)
        thread.start()

    def click(self, coordinates, button="left"):
        
        left, top, right, bottom = self.board[coordinates[1], coordinates[0]]


        #For Macs with Retna display - there are 4 pixels per mouse coordinate
        # Divide pixel by 2 to get correct mouse coordinate
        x = ((left + right) // 2) // 2
        y = ((bottom + top) // 2) // 2

        pyautogui.click(x, y, button=button)

    def read_board(self):
        # Take a screenshot of the whole board once
        tile_image = pyautogui.screenshot()

        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):

                if self.game_state[j, i] == CELL_EXPLOADED_MINE:
                    self.status = "lost"
                    return
                    
                if self.game_state[j, i] == 0:

                    # If all the mines have been found, then any covered squares can be clicked
                    if len(self.mines) == self.mine_count:
                        self.click((j, i))
                        continue

                    left, top, right, bottom = self.board[i, j]
                    
                    # Crop the relevant section from the screenshot
                    cropped = tile_image.crop((left, top, right, bottom))
                    
                    tile = identify_tile(cropped)
                    if tile == 10:
                        filename = f"./tiles/unknown{i}-{j}.png"
                        cropped.save(filename)
                        self.game_state[j, i] = -999
                    else:
                        self.game_state[j, i] = tile


    def deduce_obvious_mines(self, coordinates):
        x, y = coordinates
        cell_value = self.game_state[y, x]
        covered = []
        if x > 0:
            if self.game_state[y, x - 1] == -1:
                cell_value -= 1
            elif self.game_state[y, x - 1] == 0:
                covered.append((y, x - 1))
        
        if y > 0:
            if self.game_state[y - 1, x] == -1:
                cell_value -= 1
            elif self.game_state[y - 1, x] == 0:
                covered.append((y - 1 , x))
        
        if y > 0 and x > 0:
            if self.game_state[y - 1, x - 1] == -1:
                cell_value -= 1
            elif self.game_state[y - 1, x - 1] == 0:
                covered.append((y - 1, x - 1))
        
        if y > 0 and x < self.board_size[0] - 1:
            if self.game_state[y - 1, x + 1] == -1:
                cell_value -= 1
            elif self.game_state[y - 1, x + 1] == 0:
                covered.append((y - 1, x + 1))
        
        if x > 0 and y < self.board_size[0] - 1:
            if self.game_state[y + 1, x - 1] == -1:
                cell_value -= 1
            elif self.game_state[y + 1, x - 1] == 0:
                covered.append((y + 1, x - 1))
        
        if y < self.board_size[0] - 1 and x < self.board_size[0] - 1:
            if self.game_state[y + 1, x + 1] == -1:
                cell_value -= 1
            elif self.game_state[y + 1, x + 1] == 0:
                covered.append((y + 1, x + 1))
        
        if y < self.board_size[0] - 1:
            if self.game_state[y + 1, x] == -1:
                cell_value -= 1
            elif self.game_state[y + 1, x] == 0:
                covered.append((y + 1, x))

        if x < self.board_size[0] - 1:
            if self.game_state[y, x + 1] == -1:
                cell_value -= 1
            elif self.game_state[y, x + 1] == 0:
                covered.append((y, x + 1))

        if cell_value == len(covered):
            self.mines.update(covered)
            for mine in covered:
                if not self.game_state[mine[0], mine[1]] == CELL_MINE:
                    self.click(mine, button="right")
                    self.game_state[mine[0], mine[1]] = CELL_MINE

    def find_safe_move(self, coordinates):
        x, y = coordinates
        cell_value = self.game_state[y, x]
        covered = []
        if x > 0:
            if self.game_state[y, x - 1] == -1:
                cell_value -= 1
            elif self.game_state[y, x - 1] == 0:
                covered.append((y, x - 1))
        
        if y > 0:
            if self.game_state[y - 1, x] == -1:
                cell_value -= 1
            elif self.game_state[y - 1, x] == 0:
                covered.append((y - 1 , x))
        
        if y > 0 and x > 0:
            if self.game_state[y - 1, x - 1] == -1:
                cell_value -= 1
            elif self.game_state[y - 1, x - 1] == 0:
                covered.append((y - 1, x - 1))
        
        if y > 0 and x < self.board_size[0] - 1:
            if self.game_state[y - 1, x + 1] == -1:
                cell_value -= 1
            elif self.game_state[y - 1, x + 1] == 0:
                covered.append((y - 1, x + 1))
        
        if x > 0 and y < self.board_size[0] - 1:
            if self.game_state[y + 1, x - 1] == -1:
                cell_value -= 1
            elif self.game_state[y + 1, x - 1] == 0:
                covered.append((y + 1, x - 1))
        
        if y < self.board_size[0] - 1 and x < self.board_size[0] - 1:
            if self.game_state[y + 1, x + 1] == -1:
                cell_value -= 1
            elif self.game_state[y + 1, x + 1] == 0:
                covered.append((y + 1, x + 1))
        
        if y < self.board_size[0] - 1:
            if self.game_state[y + 1, x] == -1:
                cell_value -= 1
            elif self.game_state[y + 1, x] == 0:
                covered.append((y + 1, x))

        if x < self.board_size[0] - 1:
            if self.game_state[y, x + 1] == -1:
                cell_value -= 1
            elif self.game_state[y, x + 1] == 0:
                covered.append((y, x + 1))

        if cell_value == 0:
            return covered
        return []
        
    def determine_move(self):
        safe_set = set([])
        covered_unkown = []
        for i in range(self.board_size[1]):
            for j in range(self.board_size[0]):
                if self.game_state[j, i] == 0:
                    covered_unkown.append((i, j))
                    continue

                self.deduce_obvious_mines((i, j))
                safe = self.find_safe_move((i, j))
                safe_set.update(safe)
        if len(safe_set) > 0:
            return safe_set
        else:
            random = self.guess(covered_unkown)
            print(covered_unkown)
            print(random)
            return [random]
    
    def guess(self, covered):
        return random.choice(covered)



                
                

game = MinesweeperBot()

#once to bring into focus
game.keyboard_listener()
game.click((0, 0))

game.click((3, 5))

while len(game.mines) < game.mine_count or game.status == "playing":
    game.read_board()
    safe = game.determine_move()

    if len(safe) == 0:
        game.guess()

    for cell in safe:
        game.click(cell)



game.read_board()




