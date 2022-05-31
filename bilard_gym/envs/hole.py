import os, sys, random
import pygame, pymunk
from .CONST import *
from .ball import *

class Hole():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = center
        self.shape = pymunk.Circle(self.body , self.radius - SIZE_BALL)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = 60

        self.is_hit = False

    def hit(self):
        self.is_hit = True
    
    def reset_hit(self):
        self.is_hit = False
        
    def add_to_pymunk_space(self, pymunk_space):
        pymunk_space.add(self.body, self.shape)
    
    def remove_from_pymunk_space(self, pymunk_space):
        pymunk_space.remove(self.body, self.shape)

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, convert_coordinates(self.center) , self.radius)

    


#################### INITIALIZING HOLES
hole_bottom_left    = Hole((LEFT_BOTTOM_CORNER[0] - 30, LEFT_BOTTOM_CORNER[1] - 30) , 50)
hole_bottom_center  = Hole((LEFT_BOTTOM_CORNER[0] + WIDTH_TABLE/2, LEFT_BOTTOM_CORNER[1] - 40) , 40)
hole_bottom_right   = Hole((RIGHT_BOTTOM_CORNER[0] + 30, RIGHT_BOTTOM_CORNER[1] - 30), 50)

hole_upper_left     = Hole((LEFT_UPPER_CORNER[0] - 30 , LEFT_UPPER_CORNER[1] + 30) , 50)
hole_upper_center   = Hole((LEFT_UPPER_CORNER[0] + WIDTH_TABLE/2, LEFT_UPPER_CORNER[1] + 40) , 40)
hole_upper_right     = Hole((RIGHT_UPPER_CORNER[0] + 30 , RIGHT_UPPER_CORNER[1] + 30) , 50)

all_holes = (hole_bottom_left, hole_bottom_center, hole_bottom_right, hole_upper_left, hole_upper_center, hole_upper_right)

##################### INITIALIZING COLLISION HANLDERS



