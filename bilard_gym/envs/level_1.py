from .ball import *
from random import randint

def _place_ball_random(pymunk_space, ball):
    ball.is_in_hole = 0
    ball.body.position = randint(LEFT_BOTTOM_CORNER[0] + SIZE_BALL + 10,
                                 RIGHT_BOTTOM_CORNER[0] - SIZE_BALL - 10), randint(
        LEFT_BOTTOM_CORNER[1] + SIZE_BALL + 10, LEFT_UPPER_CORNER[1] - SIZE_BALL - 10)
    ball.body.velocity = 0, 0
    ball.add_to_pymunk_space(pymunk_space)


def place_one_ball_random_full(pymunk_space, ball_to_place):
    for ball in all_balls_full:
        if ball == ball_to_place:
            _place_ball_random(pymunk_space, ball)
        else:
            ball.is_in_hole = True
            ball.body.position = (3500, 2 * (SIZE_BALL + 2) * ball.shape.collision_type + SIZE_BALL)
            ball.body.velocity = 0, 0
            ball.add_to_pymunk_space(pymunk_space)

    for ball in all_balls_stripes:
        ball.is_in_hole = True
        ball.body.position = (3500, 2 * (SIZE_BALL + 2) * ball.shape.collision_type + SIZE_BALL)
        ball.body.velocity = 0, 0
        ball.add_to_pymunk_space(pymunk_space)
    while True:
        white_ball_full.body.position = randint(LEFT_BOTTOM_CORNER[0] + SIZE_BALL, RIGHT_BOTTOM_CORNER[0] - SIZE_BALL),\
                                        randint(LEFT_BOTTOM_CORNER[1] + SIZE_BALL, LEFT_UPPER_CORNER[1] - SIZE_BALL)
        white_ball_full.body.velocity = 0, 0
        white_ball_full.is_in_hole = False

        if white_ball_full.body.position[0] - 3 * SIZE_BALL > ball_to_place.body.position[0]:
            white_ball_full.add_to_pymunk_space(pymunk_space)
            return
        if white_ball_full.body.position[0] + 3 * SIZE_BALL < ball_to_place.body.position[0]:
            white_ball_full.add_to_pymunk_space(pymunk_space)
            return
        if white_ball_full.body.position[1] - 3 * SIZE_BALL > ball_to_place.body.position[1]:
            white_ball_full.add_to_pymunk_space(pymunk_space)
            return
        if white_ball_full.body.position[1] + 3 * SIZE_BALL < ball_to_place.body.position[1]:
            white_ball_full.add_to_pymunk_space(pymunk_space)
            return
