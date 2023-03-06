from turtle import Turtle

class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("black")
        self.shapesize(stretch_len=8, stretch_wid=1)
        self.penup()
        self.goto(0,-250)

    def go_left(self):
        new_x = self.xcor() - 30
        self.goto(new_x, self.ycor())

    def go_right(self):
        new_x = self.xcor() + 30
        self.goto(new_x, self.ycor())
