from lib2to3.pytree import convert
import os, sys, random
import pygame, pymunk
from .CONST import *
from .raycasting import Vector, intersect
from pymunk import Vec2d
from math import sqrt
from .table import table


class Ball:
    def __init__(self, center, color, collision_type):
        self.saved_velocity = None
        self.center = center
        self.color = color
        self.body = pymunk.Body()
        self.body.position = center
        self.shape = pymunk.Circle(self.body, SIZE_BALL)
        self.shape.mass = MASS
        self.shape.elasticity = ELASTICITY
        self.shape.density = DENCITY
        self.shape.friction = 1
        self.shape.collision_type = collision_type

        self.score = 0
        self.is_hit = False
        self.is_in_hole = False
        self.saved_velocity = None
        self.saved_position = None

    def add_to_pymunk_space(self,space):
        space.add(self.body, self.shape)

    def remove_from_pymunk_space(self, pymunk_space):
        pymunk_space.remove(self.body, self.shape)

    def hit_ball(self, power):
        self.body.apply_force_at_local_point(power)
        
    def in_hole(self, arbiter, space, data):
        self.is_in_hole = True
        self.body.position = 3 * SIZE_BALL, 2 * (SIZE_BALL + 2) * self.shape.collision_type + SIZE_BALL
        self.body.velocity = 0, 0

    def white_ball_col(self, d_endarbiter, space, data):
        if self.is_hit is False:
            self.is_hit = True
            self.saved_velocity = self.body.velocity
            self.saved_position = self.body.position


    def ball_table_col(self, arbiter, space, data):
        pass

    def moving(self):
        if self.body.velocity[0] == 0 and self.body.velocity[1] == 0:
            return True
        return False

    def check_pos(self):
        if self.is_in_hole == 0 and (self.body.position[0] < LEFT_BOTTOM_CORNER[0] or self.body.position[0] > RIGHT_BOTTOM_CORNER[0]):
            self.body.position  = self.center
            self.body.velocity = 0,0
            self.score -= 400
            return
        
        
        
        if  self.is_in_hole == 0 and (self.body.position[1] < LEFT_BOTTOM_CORNER[1] or self.body.position[1] > LEFT_UPPER_CORNER[1]):
            self.body.position  = self.center
            self.body.velocity = 0,0
            self.score -= 400
            return
    

class BallStripes(Ball):
    def draw(self, screen):
        pygame.draw.circle( screen , self.color , convert_coordinates(self.body.position) , SIZE_BALL , True , False , False , False)
        pygame.draw.line( screen , self.color , convert_coordinates(self.body.position - (SIZE_BALL,0)) , convert_coordinates(self.body.position + (SIZE_BALL,0)))


class BallFulls(Ball):
    def draw(self, screen):
        pygame.draw.circle( screen , self.color , convert_coordinates(self.body.position) , SIZE_BALL , True , False , False , False)


#################### INITIALIZING BALLS
yellow_ball_full    = BallFulls(POS_1ST, YELLOW , 1)
blue_ball_full      = BallFulls(POS_2ND, BLUE   , 2)
red_ball_full       = BallFulls(POS_3RD, RED    , 3)
purple_ball_full    = BallFulls(POS_4TH, PURPLE , 4)
orange_ball_full    = BallFulls(POS_5TH, ORANGE , 5)
green_ball_full     = BallFulls(POS_6TH, GREEN  , 6)
brown_ball_full     = BallFulls(POS_7TH, BROWN  , 7)

black_ball_full = BallFulls(POS_8TH, BLACK, 8)

yellow_ball_stripes = BallStripes(POS_9TH  , YELLOW , 9)
blue_ball_stripes   = BallStripes(POS_10TH , BLUE   , 10)
red_ball_stripes    = BallStripes(POS_11TH , RED    , 11)
purple_ball_stripes = BallStripes(POS_12TH , PURPLE , 12)
orange_ball_stripes = BallStripes(POS_13TH , ORANGE , 13)
green_ball_stripes  = BallStripes(POS_14TH , GREEN  , 14)
brown_ball_stripes  = BallStripes(POS_15TH , BROWN  , 15)

white_ball_full     = BallFulls(POS_16TH, WHITE, 16)

all_balls = (yellow_ball_full, blue_ball_full,
                red_ball_full, purple_ball_full, 
                orange_ball_full, green_ball_full,
                brown_ball_full , black_ball_full, 
                yellow_ball_stripes, blue_ball_stripes, 
                red_ball_stripes, purple_ball_stripes, 
                orange_ball_stripes, green_ball_stripes, 
                brown_ball_stripes, white_ball_full)

all_balls_full = (yellow_ball_full, blue_ball_full,
                red_ball_full, purple_ball_full, 
                orange_ball_full, green_ball_full,
                brown_ball_full , black_ball_full)

all_balls_stripes = (yellow_ball_stripes, blue_ball_stripes, 
                    red_ball_stripes, purple_ball_stripes, 
                    orange_ball_stripes, green_ball_stripes, 
                    brown_ball_stripes)

all_balls_string = ('yellow_ball_full', 'blue_ball_full',
                'red_ball_full', 'purple_ball_full', 
                'orange_ball_full', 'green_ball_full',
                'brown_ball_full' , 'black_ball_full', 
                'yellow_ball_stripes', 'blue_ball_stripes', 
                'red_ball_stripes', 'purple_ball_stripes', 
                'orange_ball_stripes', 'green_ball_stripes', 
                'brown_ball_stripes', 'white_ball_full')

all_balls_wo_white = (yellow_ball_full, blue_ball_full,
                red_ball_full, purple_ball_full, 
                orange_ball_full, green_ball_full,
                brown_ball_full , black_ball_full, 
                yellow_ball_stripes, blue_ball_stripes, 
                red_ball_stripes, purple_ball_stripes, 
                orange_ball_stripes, green_ball_stripes, 
                brown_ball_stripes)