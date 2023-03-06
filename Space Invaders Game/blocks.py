from turtle import Turtle
import random

ROWS = 4
GROUPS = 6

FULL_WIDTH = 900
MARGIN = 100
WIDTH = FULL_WIDTH - 2*MARGIN

DIVIDER = 60
HOVER_LOCATION = -150

class Blocks(Turtle):

    def __init__(self):
        self.all_blocks = []
        self.blocks_init()

    def blocks_init(self):
        block_total = WIDTH - (GROUPS-1)*DIVIDER
        blocks = []
        for i in range(GROUPS-1):
            block_width = random.randint(0,block_total)
            block_total -= block_width
            if block_width == 0:
                block_width = 1
            blocks.append(block_width)
        if block_total == 0:
            block_total = 1
        blocks.append(block_total)

        x_start = -1 * WIDTH/2
        y_start = HOVER_LOCATION
        for block in blocks:
            for row in range(ROWS):
                    in_block = True
                    x = 0
                    while in_block:
                        br = Turtle("square")
                        br.color("SlateGray")
                        br.penup()
                        br.shapesize(stretch_len=1, stretch_wid=1)
                        position = (x_start + x, y_start + 21*row)
                        br.goto(position)
                        self.all_blocks.append(br)

                        x += 21
                        if x > block:
                            in_block = False
            x_start += (block + DIVIDER)


    def clear_blocks(self):
        for block in self.all_blocks:
            block.hideturtle()
            self.all_blocks.remove(block)
