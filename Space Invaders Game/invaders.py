from turtle import Turtle
import random

ROWS = 4
COLUMNS = 7

RADIUS = 24 # size of each invader

X_OFFSET = -200 # invaders start position
Y_OFFSET = 300 # invaders start position

MOVE_STEPS = 11 # number of steps to move from left to right
STEP = 10 # invader's movement step size

DIFFICULTY = 10 # 1-1000 level of difficulty 
SHOT_SPEED = 30

class Invaders(Turtle):

    def __init__(self):
        super().__init__()
        self.all_invaders = []
        self.all_shots = []
        self.invaders_init()
        self.direction = 1
        self.step = 6 
        self.shot_prob = DIFFICULTY

    def invaders_init(self):
        x_pos = X_OFFSET
        y_pos = Y_OFFSET
        for row in range(ROWS):
            for column in range(COLUMNS):
                invader = Turtle()
                invader.shape("invader.gif")
                invader.penup()
                invader.goto(x_pos, y_pos)
                x_pos += RADIUS*3
                self.all_invaders.append(invader)
            x_pos = X_OFFSET    
            y_pos -= RADIUS*3          

    def clear_invaders(self):
        for invader in self.all_invaders:
            invader.hideturtle()

    def move(self):
        for invader in self.all_invaders:
            invader.goto(invader.xcor() + (self.direction * STEP), invader.ycor())
        self.step += self.direction 
        if self.step == 11:
            self.direction = -1
        elif self.step == 0:
            self.direction = 1

    def go_closer(self):
        for invader in self.all_invaders:
            invader.goto(invader.xcor(), invader.ycor() - STEP)
        print("we are getting closer :> ")    

    def shot(self):
        for invader in self.all_invaders:
            rand = random.randint(0, 1000)
            if  rand < self.shot_prob:
                new_shot = Turtle("rocket_down")
                new_shot.hideturtle()
                new_shot.color("red")
                new_shot.shapesize(1)
                new_shot.penup()
                new_shot.goto(invader.xcor(), invader.ycor())
                new_shot.showturtle()
                self.all_shots.append(new_shot)
                break

    def shots_move(self):
        for shot in self.all_shots:
            shot.goto(shot.xcor(), shot.ycor() - SHOT_SPEED)

    def level_up(self):
        self.shot_prob += 10
        print(f"level: {self.shot_prob} / 1000")