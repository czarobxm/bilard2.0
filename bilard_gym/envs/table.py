import os, sys, random
import pygame, pymunk
from .CONST import *
from .raycasting import Vector
from pymunk import Vec2d


def move(point, x):
    return point[0] + x[0], point[1] + x[1]


class Table():
    def __init__(self):
        thickness = 500

        # FLOOR LEFT
        self.body_floor_left = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_floor_left = pymunk.Poly(self.body_floor_left,
                                            [TABLE_BOTTOM_LEFT_WALL[0],
                                             TABLE_BOTTOM_LEFT_WALL[1],
                                             move(TABLE_BOTTOM_LEFT_WALL[1], (0, -thickness)),
                                             move(TABLE_BOTTOM_LEFT_WALL[0], (0, -thickness))]
                                            )
        # FLOOR RIGHT
        self.body_floor_right = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_floor_right = pymunk.Poly(self.body_floor_right,
                                            [TABLE_BOTTOM_RIGHT_WALL[0],
                                             TABLE_BOTTOM_RIGHT_WALL[1],
                                             move(TABLE_BOTTOM_RIGHT_WALL[1], (0, -thickness)),
                                             move(TABLE_BOTTOM_RIGHT_WALL[0], (0, -thickness))]
                                            )

        # FLOOR CENTER
        self.body_floor_center = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_floor_center = pymunk.Poly(self.body_floor_center,
                                            [move(TABLE_BOTTOM_LEFT_WALL[1], (0, -50)),
                                             move(TABLE_BOTTOM_RIGHT_WALL[0], (0, -50)),
                                             move(TABLE_BOTTOM_RIGHT_WALL[0], (0, -thickness)),
                                             move(TABLE_BOTTOM_LEFT_WALL[1], (0, -thickness))]
                                            )

        # WALL LEFT
        self.body_left_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_left_wall = pymunk.Poly(self.body_left_wall,
                                              [TABLE_SIDE_LEFT_WALL[0],
                                               TABLE_SIDE_LEFT_WALL[1],
                                               move(TABLE_SIDE_LEFT_WALL[1], (-thickness, 0)),
                                               move(TABLE_SIDE_LEFT_WALL[0], (-thickness, 0))]
                                              )

        # WALL RIGHT
        self.body_right_wall = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_right_wall = pymunk.Poly(self.body_right_wall,
                                           [TABLE_SIDE_RIGHT_WALL[0],
                                            TABLE_SIDE_RIGHT_WALL[1],
                                            move(TABLE_SIDE_RIGHT_WALL[1], (thickness, 0)),
                                            move(TABLE_SIDE_RIGHT_WALL[0], (thickness, 0))]
                                           )

        # CEILING LEFT
        self.body_ceiling_left = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_ceiling_left = pymunk.Poly(self.body_ceiling_left,
                                            [TABLE_UPPER_LEFT_WALL[0],
                                             TABLE_UPPER_LEFT_WALL[1],
                                             move(TABLE_UPPER_LEFT_WALL[1], (0, thickness)),
                                             move(TABLE_UPPER_LEFT_WALL[0], (0, thickness))]
                                            )

        # CEILING RIGHT
        self.body_ceiling_right = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_ceiling_right= pymunk.Poly(self.body_ceiling_right,
                                              [TABLE_UPPER_RIGHT_WALL[0],
                                               TABLE_UPPER_RIGHT_WALL[1],
                                               move(TABLE_UPPER_RIGHT_WALL[1], (0, thickness)),
                                               move(TABLE_UPPER_RIGHT_WALL[0], (0, thickness))]
                                              )

        # CEILING CENTER
        self.body_ceiling_center = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_ceiling_center = pymunk.Poly(self.body_ceiling_center,
                                              [move(TABLE_UPPER_LEFT_WALL[1], (0, 50)),
                                               move(TABLE_UPPER_RIGHT_WALL[0], (0, 50)),
                                               move(TABLE_UPPER_RIGHT_WALL[0], (0, thickness)),
                                               move(TABLE_UPPER_LEFT_WALL[1], (0, thickness))]
                                              )

        # HOLES bottom
        self.body_hole_bottom_left_one = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_bottom_left_one = pymunk.Segment(self.body_hole_bottom_left_one, HOLE_BOTTOM_LEFT_WALL_ONE[0],
                                                         HOLE_BOTTOM_LEFT_WALL_ONE[1], 1)

        self.body_hole_bottom_left_two = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_bottom_left_two = pymunk.Segment(self.body_hole_bottom_left_two, HOLE_BOTTOM_LEFT_WALL_TWO[0],
                                                         HOLE_BOTTOM_LEFT_WALL_TWO[1], 1)

        self.body_hole_bottom_center_one = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_bottom_center_one = pymunk.Segment(self.body_hole_bottom_center_one,
                                                           HOLE_BOTTOM_CENTER_WALL_ONE[0],
                                                           HOLE_BOTTOM_CENTER_WALL_ONE[1], 1)

        self.body_hole_bottom_center_two = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_bottom_center_two = pymunk.Segment(self.body_hole_bottom_center_two,
                                                           HOLE_BOTTOM_CENTER_WALL_TWO[0],
                                                           HOLE_BOTTOM_CENTER_WALL_TWO[1], 1)

        self.body_hole_bottom_right_one = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_bottom_right_one = pymunk.Segment(self.body_hole_bottom_right_one,
                                                          HOLE_BOTTOM_RIGHT_WALL_ONE[0], HOLE_BOTTOM_RIGHT_WALL_ONE[1],
                                                          1)

        self.body_hole_bottom_right_two = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_bottom_right_two = pymunk.Segment(self.body_hole_bottom_right_two,
                                                          HOLE_BOTTOM_RIGHT_WALL_TWO[0], HOLE_BOTTOM_RIGHT_WALL_TWO[1],
                                                          1)

        # HOLES upper
        self.body_hole_upper_left_one = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_upper_left_one = pymunk.Segment(self.body_hole_upper_left_one, HOLE_UPPER_LEFT_WALL_ONE[0],
                                                        HOLE_UPPER_LEFT_WALL_ONE[1], 1)

        self.body_hole_upper_left_two = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_upper_left_two = pymunk.Segment(self.body_hole_upper_left_two, HOLE_UPPER_LEFT_WALL_TWO[0],
                                                        HOLE_UPPER_LEFT_WALL_TWO[1], 1)

        self.body_hole_upper_center_one = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_upper_center_one = pymunk.Segment(self.body_hole_upper_center_one,
                                                          HOLE_UPPER_CENTER_WALL_ONE[0], HOLE_UPPER_CENTER_WALL_ONE[1],
                                                          1)

        self.body_hole_upper_center_two = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_upper_center_two = pymunk.Segment(self.body_hole_upper_center_two,
                                                          HOLE_UPPER_CENTER_WALL_TWO[0], HOLE_UPPER_CENTER_WALL_TWO[1],
                                                          1)

        self.body_hole_upper_right_one = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_upper_right_one = pymunk.Segment(self.body_hole_upper_right_one, HOLE_UPPER_RIGHT_WALL_ONE[0],
                                                         HOLE_UPPER_RIGHT_WALL_ONE[1], 1)

        self.body_hole_upper_right_two = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape_hole_upper_right_two = pymunk.Segment(self.body_hole_upper_right_two, HOLE_UPPER_RIGHT_WALL_TWO[0],
                                                         HOLE_UPPER_RIGHT_WALL_TWO[1], 1)

        # COLLISION TYPE
        # walls
        self.shape_floor_left.collision_type = 50
        self.shape_floor_right.collision_type = 50
        self.shape_floor_center.collision_type = 50
        self.shape_left_wall.collision_type = 50
        self.shape_right_wall.collision_type = 50
        self.shape_ceiling_left.collision_type = 50
        self.shape_ceiling_right.collision_type = 50
        self.shape_ceiling_center.collision_type = 50
        # bottom holes
        self.shape_hole_bottom_left_one.collision_type = 50
        self.shape_hole_bottom_left_two.collision_type = 50
        self.shape_hole_bottom_center_one.collision_type = 50
        self.shape_hole_bottom_center_two.collision_type = 50
        self.shape_hole_bottom_right_one.collision_type = 50
        self.shape_hole_bottom_right_two.collision_type = 50
        # upper holes
        self.shape_hole_upper_left_one.collision_type = 50
        self.shape_hole_upper_left_two.collision_type = 50
        self.shape_hole_upper_center_one.collision_type = 50
        self.shape_hole_upper_center_two.collision_type = 50
        self.shape_hole_upper_right_one.collision_type = 50
        self.shape_hole_upper_right_two.collision_type = 50

        # ELASTICITY
        # walls
        self.shape_floor_left.elasticity = ELASTICITY_TABLE
        self.shape_floor_right.elasticity = ELASTICITY_TABLE
        self.shape_floor_center.elasticity = ELASTICITY_TABLE
        self.shape_left_wall.elasticity = ELASTICITY_TABLE
        self.shape_right_wall.elasticity = ELASTICITY_TABLE
        self.shape_ceiling_left.elasticity = ELASTICITY_TABLE
        self.shape_ceiling_right.elasticity = ELASTICITY_TABLE
        self.shape_ceiling_center.elasticity = ELASTICITY_TABLE
        # bottom holes
        self.shape_hole_bottom_left_one.elasticity = ELASTICITY_TABLE
        self.shape_hole_bottom_left_two.elasticity = ELASTICITY_TABLE
        self.shape_hole_bottom_center_one.elasticity = ELASTICITY_TABLE
        self.shape_hole_bottom_center_two.elasticity = ELASTICITY_TABLE
        self.shape_hole_bottom_right_one.elasticity = ELASTICITY_TABLE
        self.shape_hole_bottom_right_two.elasticity = ELASTICITY_TABLE
        # upper holes
        self.shape_hole_upper_left_one.elasticity = ELASTICITY_TABLE
        self.shape_hole_upper_left_two.elasticity = ELASTICITY_TABLE
        self.shape_hole_upper_center_one.elasticity = ELASTICITY_TABLE
        self.shape_hole_upper_center_two.elasticity = ELASTICITY_TABLE
        self.shape_hole_upper_right_one.elasticity = ELASTICITY_TABLE
        self.shape_hole_upper_right_two.elasticity = ELASTICITY_TABLE

    def add_to_pymunk_space(self, pymunk_space):
        # ADDING TO PYMUNK SPACE
        # walls
        pymunk_space.add(self.body_ceiling_left, self.shape_ceiling_left)
        pymunk_space.add(self.body_ceiling_right, self.shape_ceiling_right)
        pymunk_space.add(self.body_ceiling_center, self.shape_ceiling_center)
        pymunk_space.add(self.body_floor_left, self.shape_floor_left)
        pymunk_space.add(self.body_floor_right, self.shape_floor_right)
        pymunk_space.add(self.body_floor_center, self.shape_floor_center)
        pymunk_space.add(self.body_left_wall, self.shape_left_wall)
        pymunk_space.add(self.body_right_wall, self.shape_right_wall)
        # bottom holes
        pymunk_space.add(self.shape_hole_bottom_left_one, self.body_hole_bottom_left_one)
        pymunk_space.add(self.shape_hole_bottom_left_two, self.body_hole_bottom_left_two)
        pymunk_space.add(self.shape_hole_bottom_center_one, self.body_hole_bottom_center_one)
        pymunk_space.add(self.shape_hole_bottom_center_two, self.body_hole_bottom_center_two)
        pymunk_space.add(self.shape_hole_bottom_right_one, self.body_hole_bottom_right_one)
        pymunk_space.add(self.shape_hole_bottom_right_two, self.body_hole_bottom_right_two)
        # upper holes
        pymunk_space.add(self.shape_hole_upper_left_one, self.body_hole_upper_left_one)
        pymunk_space.add(self.shape_hole_upper_left_two, self.body_hole_upper_left_two)
        pymunk_space.add(self.shape_hole_upper_center_one, self.body_hole_upper_center_one)
        pymunk_space.add(self.shape_hole_upper_center_two, self.body_hole_upper_center_two)
        pymunk_space.add(self.shape_hole_upper_right_one, self.body_hole_upper_right_one)
        pymunk_space.add(self.shape_hole_upper_right_two, self.body_hole_upper_right_two)

    def remove_from_pymunk_space(self, pymunk_space):
        # walls
        pymunk_space.remove(self.body_ceiling_left, self.shape_ceiling_left)
        pymunk_space.remove(self.body_ceiling_right, self.shape_ceiling_right)
        pymunk_space.remove(self.body_ceiling_center, self.shape_ceiling_center)
        pymunk_space.remove(self.body_floor_left, self.shape_floor_left)
        pymunk_space.remove(self.body_floor_right, self.shape_floor_right)
        pymunk_space.remove(self.body_floor_center, self.shape_floor_center)
        pymunk_space.remove(self.body_left_wall, self.shape_left_wall)
        pymunk_space.remove(self.body_right_wall, self.shape_right_wall)
        # bottom holes
        pymunk_space.remove(self.shape_hole_bottom_left_one, self.body_hole_bottom_left_one)
        pymunk_space.remove(self.shape_hole_bottom_left_two, self.body_hole_bottom_left_two)
        pymunk_space.remove(self.shape_hole_bottom_center_one, self.body_hole_bottom_center_one)
        pymunk_space.remove(self.shape_hole_bottom_center_two, self.body_hole_bottom_center_two)
        pymunk_space.remove(self.shape_hole_bottom_right_one, self.body_hole_bottom_right_one)
        pymunk_space.remove(self.shape_hole_bottom_right_two, self.body_hole_bottom_right_two)
        # upper holes
        pymunk_space.remove(self.shape_hole_upper_left_one, self.body_hole_upper_left_one)
        pymunk_space.remove(self.shape_hole_upper_left_two, self.body_hole_upper_left_two)
        pymunk_space.remove(self.shape_hole_upper_center_one, self.body_hole_upper_center_one)
        pymunk_space.remove(self.shape_hole_upper_center_two, self.body_hole_upper_center_two)
        pymunk_space.remove(self.shape_hole_upper_right_one, self.body_hole_upper_right_one)
        pymunk_space.remove(self.shape_hole_upper_right_two, self.body_hole_upper_right_two)

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_EDGE,
                         (OFFSET_SCREEN_WIDTH - 30, OFFSET_SCREEN_LENGTH - 30, WIDTH_TABLE + 60, LENGTH_TABLE + 60), 0)
        pygame.draw.rect(screen, COLOR_BOARD, (OFFSET_SCREEN_WIDTH, OFFSET_SCREEN_LENGTH, WIDTH_TABLE, LENGTH_TABLE), 0)

        pygame.draw.line(screen, YELLOW, TABLE_BOTTOM_LEFT_WALL[0], TABLE_BOTTOM_LEFT_WALL[1], 1)
        pygame.draw.line(screen, BLACK, TABLE_BOTTOM_RIGHT_WALL[0], TABLE_BOTTOM_RIGHT_WALL[1], 1)
        pygame.draw.line(screen, BLACK, TABLE_UPPER_LEFT_WALL[0], TABLE_UPPER_LEFT_WALL[1], 1)
        pygame.draw.line(screen, BLACK, TABLE_UPPER_RIGHT_WALL[0], TABLE_UPPER_RIGHT_WALL[1], 1)
        pygame.draw.line(screen, BLACK, TABLE_SIDE_LEFT_WALL[0], TABLE_SIDE_LEFT_WALL[1], 1)
        pygame.draw.line(screen, BLACK, TABLE_SIDE_RIGHT_WALL[0], TABLE_SIDE_RIGHT_WALL[1], 1)

        pygame.draw.line(screen, BLACK, HOLE_BOTTOM_LEFT_WALL_ONE[0], HOLE_BOTTOM_LEFT_WALL_ONE[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_BOTTOM_LEFT_WALL_TWO[0], HOLE_BOTTOM_LEFT_WALL_TWO[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_BOTTOM_CENTER_WALL_ONE[0], HOLE_BOTTOM_CENTER_WALL_ONE[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_BOTTOM_CENTER_WALL_TWO[0], HOLE_BOTTOM_CENTER_WALL_TWO[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_BOTTOM_RIGHT_WALL_ONE[0], HOLE_BOTTOM_RIGHT_WALL_ONE[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_BOTTOM_RIGHT_WALL_TWO[0], HOLE_BOTTOM_RIGHT_WALL_TWO[1], 1)

        pygame.draw.line(screen, BLACK, HOLE_UPPER_LEFT_WALL_ONE[0], HOLE_UPPER_LEFT_WALL_ONE[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_UPPER_LEFT_WALL_TWO[0], HOLE_UPPER_LEFT_WALL_TWO[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_UPPER_CENTER_WALL_ONE[0], HOLE_UPPER_CENTER_WALL_ONE[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_UPPER_CENTER_WALL_TWO[0], HOLE_UPPER_CENTER_WALL_TWO[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_UPPER_RIGHT_WALL_ONE[0], HOLE_UPPER_RIGHT_WALL_ONE[1], 1)
        pygame.draw.line(screen, BLACK, HOLE_UPPER_RIGHT_WALL_TWO[0], HOLE_UPPER_RIGHT_WALL_TWO[1], 1)

    def positions(self):
        left = Vector(a=self.shape_left_wall.a, b=self.shape_left_wall.b)
        right = Vector(a=self.shape_right_wall.a, b=self.shape_right_wall.b)
        ceiling_left = Vector(a=self.shape_ceiling_left.a, b=self.shape_ceiling_left.b)
        ceiling_right = Vector(a=self.shape_ceiling_right.a, b=self.shape_ceiling_right.b)
        floor_left = Vector(a=self.shape_floor_left.a, b=self.shape_floor_left.b)
        floor_right = Vector(a=self.shape_floor_right.a, b=self.shape_floor_right.b)
        return [left, right, floor_left, floor_right, ceiling_left, ceiling_right]

    def full_positions(self):
        left_upper = Vec2d(LEFT_UPPER_CORNER[0], LEFT_UPPER_CORNER[1])
        right_upper = Vec2d(RIGHT_UPPER_CORNER[0], RIGHT_UPPER_CORNER[1])
        left_bottom = Vec2d(LEFT_BOTTOM_CORNER[0], LEFT_BOTTOM_CORNER[1])
        right_bottom = Vec2d(RIGHT_BOTTOM_CORNER[0], RIGHT_BOTTOM_CORNER[1])

        print(left_upper)

        left = Vector(a=left_bottom, b=left_upper)
        right = Vector(a=right_bottom, b=right_upper)
        ceiling = Vector(a=left_upper, b=right_upper)
        floor = Vector(a=left_bottom, b=right_bottom)
        return [left, right, floor, ceiling]

    LEFT_BOTTOM_CORNER = [OFFSET_SCREEN_WIDTH, OFFSET_SCREEN_LENGTH]
    LEFT_UPPER_CORNER = [OFFSET_SCREEN_WIDTH, SCREEN_LENGTH - OFFSET_SCREEN_LENGTH]
    RIGHT_BOTTOM_CORNER = [SCREEN_WIDTH - OFFSET_SCREEN_WIDTH, OFFSET_SCREEN_LENGTH]
    RIGHT_UPPER_CORNER = [SCREEN_WIDTH - OFFSET_SCREEN_WIDTH, SCREEN_LENGTH - OFFSET_SCREEN_LENGTH]


table = Table()
