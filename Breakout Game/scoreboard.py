from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.level = 1
        self.highscore = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        # score
        self.goto(335, 225)
        self.write(f"Score:{self.score}", align="center", font=("Courier", 24, "bold"))
        # highscore
        self.goto(-335, 225)
        self.write(f"High Score:{self.highscore}", align="center", font=("Courier", 24, "bold"))
        self.goto(0, 225)
        self.write(f"Level:{self.level}", align="center", font=("Courier", 24, "bold"))

    def point(self):
        self.score = self.score + 10*self.level
        if self.score > self.highscore:
            self.highscore = self.score
        self.update_scoreboard()

    def game_over(self):
        self.score = 0
        self.update_scoreboard()

    def win(self):
        self.level += 1
        self.update_scoreboard()