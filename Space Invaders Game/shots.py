from turtle import Turtle

MOVE = 32

class Shots(Turtle):
    def __init__(self):
        super().__init__()
        self.all_shots = []
        self.shots_init()

    def shots_init(self):
        self.all_shots = []

    def shot(self,x_cor):
        print("SHOOOOT")
        new_shot = Turtle("circle")
        new_shot.shapesize(0.75)
        new_shot.color("red")
        new_shot.penup()
        new_shot.goto(x_cor, -340)
        self.all_shots.append(new_shot)
        print(f"{new_shot.xcor()} , {new_shot.ycor()}")

    def shots_move(self):
        for shot in self.all_shots:
            shot.goto(shot.xcor(), shot.ycor() + MOVE)
