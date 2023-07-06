import numpy
import pyscreeze
from PIL import ImageDraw

from settings import BEGINNER_BOARD, EXPERT_BOARD, HARD_BOARD, MINE_COUNTS, MINESWEEPER_MACOS, MINIMUM_CELL_SIZE, SCREEN


def find_game(settings=MINESWEEPER_MACOS):
    '''Take a screenshot and scan the image to find the minesweeper game
    '''

    image = pyscreeze.screenshot()

    found = find_all_squares(image)

    if len(found) < 10:
        print(f"Cannot find game - only found {len(found)} squares")
        return numpy.array([]), [], 0, False
    
    board_size, mine_count = deduce_game_difficulty(found)
    
    if mine_count == 0:
        print(f"Invalid board size - {board_size[0]} x {board_size[1]}")
        image.show()
        return numpy.array([]), [], 0, False
    
    print(f"Found board size of {board_size[0]} x {board_size[1]} - infering mine count of {mine_count}")

    board = arrange_board(found, board_size)

    return board, board_size, mine_count, True
def find_all_squares(image):
    '''Given an image, try to find squares that match the defined field color for the game'''
    draw = ImageDraw.Draw(image)

    pixels = image.load()

    found = []


    for i in range(SCREEN.width):
        for j in range(SCREEN.height):
            if MINESWEEPER_MACOS.is_field_color(pixels[i, j]):

                left, top, right, bottom = find_square(pixels, i, j)


                if left and \
                    right - left > MINIMUM_CELL_SIZE and \
                    (bottom - top) > 0 and \
                    1.1 > (right-left) / (bottom - top) > 0.9:

                    found.append((left, top, right, bottom))

                    draw.rectangle((left, top, right, bottom), fill="green")
                else: 
                    # Paint it over, so we will not have to test
                    # these pixels again
                    draw.line((left, top, right, top), fill="white")
                    draw.line((left, top, left, bottom), fill="white")       
    return found
                    

def find_square(pixels, left, top):
    '''Given a pixel coordinates, scan right and down to determine there is a square image that is all the same color.
    Returns the pixel cordinates for the left, and right x-axis boarders and the top and bottom y-axis borders
    '''

    #start to the left and move right until pixel color change
    right = left
    while right < SCREEN.width and MINESWEEPER_MACOS.is_field_color(pixels[right + 1, top]):
        right += 1

    bottom = top
    while bottom < SCREEN.height - 1 and MINESWEEPER_MACOS.is_field_color(pixels[left , bottom + 1]):
        bottom +=  1
    
    for i in range(left, right + 1):
        for j in range(top, bottom + 1):

            if not MINESWEEPER_MACOS.is_field_color(pixels[i,j]):
                return False, False, False, False
            
    return left, top, right, bottom

def deduce_game_difficulty(found):

    # I don't know why, but for 9X9 - 81 squares are correctly found,
    # but it is coming up with a board count of 10 x 10
    print(f"Squares found: {len(found)}")

    game_width = len(set((left for left, _, _, _, in found))) -1 

    game_height = len(set((top for _, top, _, _, in found))) - 1
    mine_count =  0
    
    if (game_width, game_height) in [BEGINNER_BOARD, HARD_BOARD, EXPERT_BOARD]:
        mine_count = MINE_COUNTS[(game_width, game_height)]
    
    return (game_width, game_height), mine_count

def arrange_board(found, board_size):
    grid = numpy.array(found, dtype=object)
    grid = numpy.reshape(grid, list(board_size) + [4])
    return grid

def identify_tile(tile):
    for sample, value in MINESWEEPER_MACOS.samples:
        difference = get_difference(tile, sample)

        if difference < 3500:
            return value
    return 10
        
def get_difference(image1, image2):
    pixels1 = image1.load()
    pixels2 = image2.load()
    difference = 0
    for i in range(min(image1.size[0], image2.size[0])):
        for j in range(min(image1.size[1], image2.size[1])):
            for position in range(3):
                difference += abs(pixels1[i, j][position] -
                                    pixels2[i, j][position])
    return difference