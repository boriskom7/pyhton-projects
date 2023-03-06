from turtle import Turtle

LIVES = 3

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives_left = LIVES
        self.lives = []
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        # title
        self.penup()
        self.goto(-300, 375)
        self.color("yellow")
        self.write("Space Invaders", align="left", font=("Courier", 32, "bold"))
        self.goto(-300, 350)
        self.color("gray")
        self.write("Use cursor keys to move and 'Space' to fire", align="left", font=("Courier", 12))
        # divider line
        self.hideturtle()
        self.penup()
        self.goto(-300,-385)
        self.pendown()
        self.goto(300,-385)
        self.penup()
        # score
        self.goto(200, -425)
        self.write(f"Score:{self.score}", align="left", font=("Courier", 16, "bold"))
        # lives
        x_pos = 0
        # clear previous lives
        for live in self.lives:
            live.hideturtle()
            self.lives = []
        # set new lives
        for i in range(self.lives_left):
            live = Turtle("triangle")
            live.shapesize(1)
            live.color("white")
            live.penup()
            live.goto(-285 + x_pos, -410)
            x_pos += 35
            self.lives.append(live)

    def add_point(self):
        print("add +1 point")
        self.score += 1
        self.update_scoreboard()

    def hit(self):    
        print("hit")
        self.lives_left -= 1
        self.update_scoreboard()

    def game_over(self):
        self.clear()
        self.goto(-230, 325)
        self.color("red")
        self.write("GAME OVER!!!", align="left", font=("Courier", 48, "bold"))
        print("GAME OVER!")

