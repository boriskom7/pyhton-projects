import time
import turtle
from turtle import Screen
from spaceship import Spaceship
from invaders import Invaders
from shots import Shots
from scoreboard import Scoreboard
from blocks import Blocks

bg_img = "space_invaders BG.png"
turtle.tracer(False)

# screen settings
screen = Screen()
screen.setup(width=700, height= 900)
screen.bgpic(bg_img)
screen.bgcolor("black")
screen.title("Spcae INVADERS")
screen.delay(0.1)

# cusom shapes
screen.register_shape("invader.gif")
screen.register_shape("spaceship.gif")
screen.register_shape("shiprocket.gif")
shape =((0, 0), (-5, -5), (0, -10), (5, -10), (5, 0)) # rocket UP
screen.register_shape('rocket', shape)
shape =((0, 0), (5, 5), (10, 0), (5, -5)) # rocket DOWN
screen.register_shape('rocket_down', shape)

# initialization
spaceship = Spaceship()
invaders = Invaders()
shots = Shots()
scoreboard = Scoreboard()
blocks = Blocks()

# screen events
screen.delay(1)
screen.listen()
screen.onkey(spaceship.go_left, "Left")
screen.onkey(spaceship.go_right, "Right")
screen.onkey(spaceship.shot, "space")

# game
game_is_on = True
invaders_timer = time.time()
while game_is_on:
    time.sleep(0.25)
    turtle.update()
    # invaders movement left-right
    invaders.move()
    # invaders movement down - every 15 seconds
    if time.time() - invaders_timer > 15:
        invaders.go_closer()
        invaders_timer = time.time()

    # shots movememnt 
    spaceship.shots_move()
    invaders.shot()
    invaders.shots_move()

    # check collision with invaders
    for invader in invaders.all_invaders:
        # check SPACESHIP collision with invaders (game over condition)
        if invader.distance(spaceship) < 20:
            scoreboard.game_over()
            time.sleep(2)
            game_is_on = False
            break
        # check SHOTS collision with invaders (point addition & level-up condition)
        for shot in spaceship.all_shots:      
            if invader.distance(shot) < 30:
                # remove invader
                invader.hideturtle()
                invaders.all_invaders.remove(invader)
                # remove shot
                shot.hideturtle()
                spaceship.all_shots.remove(shot)
                # add point & level-up
                screen.delay(0.1)
                scoreboard.add_point()
                invaders.level_up()
                screen.delay(1)
                break

    # check collision with invaders' SHOTS
    for shot in invaders.all_shots:      
        if spaceship.distance(shot) < 20:
            # remove shot
            shot.hideturtle()
            invaders.all_shots.remove(shot)
            # update 'hit'
            screen.delay(0.1)
            scoreboard.hit()
            screen.delay(1)
            break        

        # check collosions between spaceship SHOTS and invaders SHOTS
        for space_shot in spaceship.all_shots:
            if space_shot.distance(shot) < 16:
                # remove invader shot
                shot.hideturtle()
                invaders.all_shots.remove(shot)
                # remove spaceship shot
                space_shot.hideturtle()
                spaceship.all_shots.remove(space_shot)
                break

    # check SHOTS collision with blocks
    # spaceship shots
    for shot in spaceship.all_shots: 
        for block in blocks.all_blocks:      
            if block.distance(shot) < 16:
                # remove invader
                block.hideturtle()
                blocks.all_blocks.remove(block)
                # remove shot
                shot.hideturtle()
                spaceship.all_shots.remove(shot)
                break
        # remove shots out of screen
        if shot.ycor() > 415:
            shot.hideturtle()
            spaceship.all_shots.remove(shot)  

    # invader shots
    for shot in invaders.all_shots: 
        for block in blocks.all_blocks:      
            if block.distance(shot) < 16:
                # remove invader
                block.hideturtle()
                blocks.all_blocks.remove(block)
                # remove shot
                shot.hideturtle()
                invaders.all_shots.remove(shot)
                break            
        # remove shots out of screen
        if shot.ycor() < -415:
            shot.hideturtle()
            invaders.all_shots.remove(shot) 

    # no lives left -> game over!
    if scoreboard.lives == []:
        scoreboard.game_over()
        time.sleep(2)
        game_is_on = False


screen.exitonclick()
