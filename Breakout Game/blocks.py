from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "gray", "teal", "magenta"]
HEIGHT = 40
WIDTH = 100
BLOCK_SIZE = 4
ROWS = 4
SQUARE = 21

class Blocks(Turtle):

    def __init__(self):
        self.all_blocks = []
        self.blocks_init()

    def blocks_init(self):
        shift = 0
        for row in range(ROWS):
            color = random.choice(COLORS)
            for column in range(-5, 6):
                block = Turtle("square")
                block.color(color)
                block.penup()
                block.shapesize(stretch_len=BLOCK_SIZE)
                position = (column*WIDTH, row*HEIGHT)
                block.goto(position)

                self.all_blocks.append(block)
            shift += 21

    def clear_blocks(self):
        for block in self.all_blocks:
            block.hideturtle()