from turtle import Turtle

SHOT_SPEED = 30

class Spaceship(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("spaceship.gif")
        self.shapesize(stretch_len=5, stretch_wid=1)
        self.penup()
        self.goto(0,-325)
        self.all_shots = []

    def go_left(self):
        new_x = self.xcor() - 30
        self.goto(new_x, self.ycor())

    def go_right(self):
        new_x = self.xcor() + 30
        self.goto(new_x, self.ycor())

    def shot(self):
        print("SHOOOOT")
        new_shot = Turtle("rocket")
        new_shot.hideturtle()
        new_shot.color("white")
        new_shot.shapesize(1)
        new_shot.penup()
        new_shot.goto(self.xcor(), -270)
        new_shot.showturtle()
        self.all_shots.append(new_shot)

    def shots_move(self):
        for shot in self.all_shots:
            shot.goto(shot.xcor(), shot.ycor() + SHOT_SPEED)