from turtle import Screen
from blocks import Blocks
from scoreboard import Scoreboard
from ball import Ball
from paddle import Paddle
import random

bg_img = random.choice(["BG1.png", "BG2.png", "BG3.png"])

screen = Screen()
screen.setup(width=1000, height= 600)
screen.bgpic(bg_img)
screen.bgcolor("black")
screen.title("Breakout")
screen.delay(0.5)


scoreboard = Scoreboard()
ball = Ball()
paddle = Paddle()
blocks = Blocks()

screen.delay(1)

screen.listen()
screen.onkey(paddle.go_left, "Left")
screen.onkey(paddle.go_right, "Right")


game_is_on = True
while game_is_on:
    screen.update()
    ball.move()

    # collision with paddle
    if ball.distance(paddle) < 30:
        ball.bounce_y()

    # collision with wall
    if ball.xcor() > 480 or ball.xcor() < -480:
        ball.bounce_x()

    if ball.ycor() > 280:
        ball.bounce_y()

    # game over
    if ball.ycor() < -280:
        screen.delay(0.5)

        scoreboard.game_over()
        blocks.clear_blocks()
        blocks.__init__()
        ball.reset_position()

        screen.delay(1)

    # collision with blocks
    for block in blocks.all_blocks:
        if block.distance(ball) < 35:
            screen.delay(0.5)

            block.hideturtle()
            blocks.all_blocks.remove(block)
            ball.bounce_y()
            scoreboard.point()

            screen.delay(1)
            break

    # win condition
    if blocks.all_blocks == []:
        screen.delay(0.5)

        scoreboard.win()
        ball.level_up(scoreboard.level)
        blocks.clear_blocks()
        blocks.__init__()
        ball.reset_position()

        screen.delay(1)

screen.exitonclick()
