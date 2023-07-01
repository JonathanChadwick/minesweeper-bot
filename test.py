import pyscreeze
from PIL import ImageDraw

image = pyscreeze.screenshot()

draw = ImageDraw.Draw(image)

draw.rectangle((1, 1, 100, 100), fill="black")

draw.line((200, 1, 300, 100), fill="black")
draw.line((200, 1, 200, 100), fill="black")

image.show()