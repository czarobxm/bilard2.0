import os, sys, random
import pygame, pymunk
import pymunk.pygame_util
import numpy as np

from .table import *
from .hole import *
from .ball import *
from .raycasting import *
from .level_1 import *
from .general import *


def closest_hole(point, all_holes):
    min_dist = None
    close_hole = None
    for hole in all_holes:
        if min_dist is None:
            min_dist = _norm(point, hole.center)
            close_hole = hole
        d = _norm(point, hole.center)
        if d < min_dist:
            min_dist = d
            close_hole = hole
    return close_hole, min_dist


def close():
    pygame.quit()


def reset_balls():
    for ball in all_balls:
        ball.is_hit = False
        ball.saved_velocity = None
        ball.saved_position = None


def friction():
    for ball in all_balls:
        friction_force(ball)


def friction_force(ball):
    if ball.body.velocity[0] > 0.2 or ball.body.velocity[1] > 0.2 or ball.body.velocity[0] < -0.2 or \
            ball.body.velocity[1] < -0.2:
        ball.body.velocity -= ball.body.velocity * 0.0098
    else:
        ball.body.velocity = 0, 0


def check_balls_pos():
    for ball in all_balls:
        ball.check_pos()


def mouse_pos():
    return pygame.mouse.get_pos()


def stopped():
    for ball in all_balls:
        if ball.body.velocity[0] != 0 or ball.body.velocity[1] != 0:
            return False
    return True


def make_action(action):
    if stopped():
        power = 25
        x1 = (action[0] + 1) / 2 * SCREEN_WIDTH
        x2 = (action[1] + 1) / 2 * SCREEN_LENGTH
        y1 = white_ball_full.body.position[0]
        y2 = white_ball_full.body.position[1]
        norm = np.sqrt((x1 - y1) ** 2 + (x2 - y2) ** 2)

        # normalized vector times power of a hit
        vel_vector = 1 / norm * (x1 - y1) * power * (action[2]+1)/2, 1 / norm * (x2 - y2) * power * (action[2]+1)/2

        if norm != 0:
            white_ball_full.body.velocity = vel_vector
        else:
            print("norma wybranego wektora ruchu == 0 ")


class Pygame2D():
    def __init__(self):
        self.show_game = False
        self.pymunk_space = pymunk.Space()
        self.add_objects_to_pymunk()

        if len(sys.argv) > 1:
            self.show_game = sys.argv[1] == 'True'

        if self.show_game:
            pygame.init()
            self.pygame_screen = pygame.display.set_mode(SCREEN_SIZE)
            self.clock = pygame.time.Clock()
            pygame.dt = 1

        # HANDLING VARIABLES THAT HAVE TO BE PASSED TO BILARD_ENV.PY
        # ex.: d_start to calculate distance difference
        # between white ball and color ball before and after move
        self.iter = 0
        self.closest_ball = None  # closest ball to chosen action point
        self.finish_score = 0
        # print(len(raycast(table=table)))

    def draw(self):
        table.draw(self.pygame_screen)

        for hole in all_holes:
            hole.draw(self.pygame_screen)

        for ball in all_balls:
            ball.draw(self.pygame_screen)

        if False:
            raycast_points = raycast(white_ball_full, table=table)

            for point in raycast_points:
                pygame.draw.line(self.pygame_screen, WHITE, convert_coordinates(white_ball_full.body.position), convert_coordinates(point))

    def refresh_screen(self):
        self.dt = self.clock.tick(FRAMERATE)
        pygame.display.flip()

    def check_events(self):
        power = 1 / 50
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            if event.type == pygame.MOUSEBUTTONUP:
                # if stopped():
                x = convert_coordinates(mouse_pos())
                white_ball_full.body.velocity = power * (x[0] - white_ball_full.body.position[0]), power * (
                            x[1] - white_ball_full.body.position[1])

    def add_objects_to_pymunk(self):

        table.add_to_pymunk_space(self.pymunk_space)

        for hole in all_holes:
            hole.add_to_pymunk_space(self.pymunk_space)

        place_one_ball_random_full(self.pymunk_space, yellow_ball_full)
        # place_balls_start(self.pymunk_space)

        for ball in all_balls_wo_white:
            self.pymunk_space.add_collision_handler(16, ball.shape.collision_type).post_solve = ball.white_ball_col
            self.pymunk_space.add_collision_handler(60, ball.shape.collision_type).post_solve = ball.in_hole

    def delete_objects_from_pymunk(self):
        table.remove_from_pymunk_space(self.pymunk_space)

        for hole in all_holes:
            hole.remove_from_pymunk_space(self.pymunk_space)

        for ball in all_balls:
            ball.remove_from_pymunk_space(self.pymunk_space)

    def game(self):
        yellow_ball_full.saved_velocity = 0,0
        while True:
            self.pymunk_space.step(1)

            self.check_events()

            self.draw()
            aim_point = 0,0

            if (yellow_ball_full.saved_velocity[0] != 0 or yellow_ball_full.saved_velocity[1] != 0):
                position = yellow_ball_full.saved_position
                velocity = yellow_ball_full.saved_velocity * (-1)

                vec = Vector(position, position + velocity)
                aim_point = intersect(vec, table)
                yellow_ball_full.is_hit = False

                chosen_hole, min_dist = closest_hole(aim_point, all_holes)
                pygame.draw.circle(self.pygame_screen, RED, convert_coordinates(chosen_hole.center), 20)

                print(min_dist)

            pygame.draw.circle(self.pygame_screen, YELLOW, convert_coordinates(aim_point), 20)
            self.refresh_screen()

            for ball in all_balls:
                friction_force(ball)

    # functions to evaluate our model

    def d_rew_1(self, scaled_action):
        return _norm(self.closest_ball.body.position, scaled_action)

    def d_rew_2(self):
        return _norm(white_ball_full.body.position, self.closest_ball.body.position)

    def evaluate(self, action, obs):
        """
        REWARDS:
        1. reward for aiming at the ball/choosing right action point
        2. reward for shooting the ball/choosing right power
        3. reward for scoring/ calculate distance between holes and a ball 
        """

        # SAVING CLOSEST BALL TO ACTION POINT AND THE DISTANCE BETWEEN THEM
        #scaled_action = (action[0] * SCREEN_WIDTH, action[1] * SCREEN_LENGTH)

        # 1.
        # reward for aiming for the ball \in [-1,0.5]

        # 2.
        # reward for shooting color balls
        # already calculated d_start. Reward will be added after all balls have stopped.

        """
          1. wybierz najbliższą kule
          2. zapisz początkową odległość: d_start
          3. wykonaj ruch
          4. zapisz odległość po ruchu: d_end
          5. reward: (d_start-d_end)/d_start 
        """

        # 3.
        # reward for scoring ball/ tactics
        # DON'T HAVE AN IDEA

        return self.finish_score

    # CHECK IF SCALED ACTION HAS TO BE A PARAMETER
    def d_end(self, scaled_action):
        """

        :param scaled_action:
        :return: distance between white
        """
        norm = _norm(self.closest_ball.body.position, scaled_action)
        return norm

    def observe(self):
        balls_pos = np.array([])
        for ball in all_balls:
            if ball.is_in_hole:
                balls_pos = np.append(balls_pos, [-1, -1, False], axis=0)
            else:
                x1 = ball.body.position[0] / SCREEN_WIDTH * 2 - 1
                x2 = ball.body.position[1] / SCREEN_LENGTH * 2 - 1
                balls_pos = np.append(balls_pos, [x1, x2, ball.is_in_hole], axis=0)
        return balls_pos

    def is_done(self, stop_moment):
        if self.iter >= stop_moment - 1:
            self.iter = stop_moment - 1
            return True
        if self.iter < stop_moment - 1:
            self.iter += 1
            return False

    def calculate_rew_2(self, d_start, d_end):
        rew_2_score = max(0, (d_start - d_end) / d_start)
        return rew_2_score

    def dist_from_hole(self, point, hole):
        return _norm(point, hole.center)


def _place_balls_random(pymunk_space):
    for ball in all_balls_wo_white:
        if random() < 0.5:
            ball.body.position = randint(LEFT_BOTTOM_CORNER[0], RIGHT_BOTTOM_CORNER[0]), randint(LEFT_BOTTOM_CORNER[1],
                                                                                                 LEFT_UPPER_CORNER[1])
            ball.body.velocity = 0, 0
            ball.add_to_pymunk_space(pymunk_space)
        else:
            ball.body.position = (3 * SIZE_BALL - 40, 2 * (SIZE_BALL + 2) * ball.shape.collision_type + SIZE_BALL)
            ball.body.velocity = 0, 0
            ball.add_to_pymunk_space(pymunk_space)

    white_ball_full.body.position = randint(LEFT_BOTTOM_CORNER[0] + SIZE_BALL,
                                            RIGHT_BOTTOM_CORNER[0] - SIZE_BALL), randint(
        LEFT_BOTTOM_CORNER[1] + SIZE_BALL, LEFT_UPPER_CORNER[1] - SIZE_BALL)
    white_ball_full.body.velocity = 0, 0
    white_ball_full.add_to_pymunk_space(pymunk_space)


def _norm(x, y):
    """
    Calculating distance between two points
    :param x: first point on surface
    :param y: second point on surface
    :return: distance between x and y
    """
    d1 = x[0] - y[0]
    d2 = x[1] - y[1]
    return np.sqrt(d1 ** 2 + d2 ** 2)


def choose_closest_ball(balls, point):
    """
    REMEMBER TO SCALE POINT TO TABLE SIZE
    choosing ball closest to the chosen point
    :param balls: list of balls
    :param point: chosen point
    :return: list: [distance, closest_ball]
    """
    x = None
    closest_ball = None
    for ball in balls:
        if ball.is_in_hole == 0:  # bother only with balls on the table
            d = _norm(ball.body.position, point)
            if x is None:  # saving first ball
                x = d
                closest_ball = ball
            else:
                if d > x:  # updating closest_ball if found closer one
                    x = d
                    closest_ball = ball
    return closest_ball
