from .ball import *

def place_balls_start(pymunk_space):
    for ball in all_balls:
        ball.body.position = ball.center
        ball.body.velocity = 0, 0
        ball.add_to_pymunk_space(pymunk_space)
