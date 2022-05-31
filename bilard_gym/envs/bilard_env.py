import gym
from gym import spaces
import numpy as np
import pygame, pymunk
import pymunk.pygame_util
from .pygame_2d import *
from .CONST import *
from .hole import all_holes


class BilardEnv(gym.Env):
    def __init__(self):
        self.bilard = Pygame2D()
        self.observation_space = spaces.Box(low=np.array(16 * [-1, -1, -1]), high=np.array(16 * [1, 1, 1]))
        self.action_space = spaces.Box(low=np.array([-1, -1, -1]), high=np.array([1, 1, 1]))

    def reset(self):
        if self.bilard.show_game:
            close()
        self.bilard.delete_objects_from_pymunk()
        self.bilard = Pygame2D()
        obs = self.bilard.observe()
        print("reset env\n")
        return obs

    def balls_stopped(self):
        return stopped()

    def step(self, action):
        """
        1. Make a move
        2. Change is_hit to False for every ball at the beginning of the move
        3. Save scaled action and save ball the model chose
        4. Calculate REWARD_1 on chosen action
        5. Calculate REWARD_2's starting distance between white ball and chosen ball
        6. For loop with game - rendering ball movements
        7. All balls have stopped.
        7. Calculate REWARD_2's ending distance between white ball and chosen ball (1 if the ball was hit)
        8. OBS, REWARD AND CHECKING IF GAME HAS ENDED
        :param action:
        :return:
        """
        print("\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # stop balls if they were generated on each other
        self.bilard.pymunk_space.step(1)
        while not stopped():
            print(yellow_ball_full.body.velocity)
            self.bilard.pymunk_space.step(1)
            friction()
            self.render(action)

        make_action(action)
        reset_balls()

        # SCALE ACTION, CHOOSE BALL AT THE BEGINNING OF THE STEP
        scaled_action = ((action[0] + 1) * SCREEN_WIDTH/2, (action[1] + 1) * SCREEN_LENGTH/2)
        self.bilard.closest_ball = choose_closest_ball(all_balls_wo_white, scaled_action)

        # REWARD 1
        d_rew_1 = self.bilard.d_rew_1(scaled_action)
        rew_1 = min(1, 50 / d_rew_1) * 1.5 - 1

        # REWARD 1_1
        vec2d_scaled_action = Vec2d(scaled_action[0], scaled_action[1])
        vec = Vector(vec2d_scaled_action, self.bilard.closest_ball.body.position)
        aim_point = intersect(vec, table)
        chosen_hole, min_dist = closest_hole(aim_point, all_holes)
        rew_1_1 = min(1, 50 / min_dist)

        # REWARD 2 - calculate starting distance
        d_start_rew_2 = self.bilard.d_rew_2()


        for i in range(500):
            # self.pygame.pymunk_space.step(1)
            self.render(action)


        print(f'action: {action}')
        print('ruch\n')
        while True:
            self.bilard.pymunk_space.step(1)
            friction()
            self.render(action)

            """
            for i in range(2):
                # self.pygame.pymunk_space.step(1)
                self.render(action)
            """

            if stopped():
                # CALCULATE REWARD 2 - if ball was hit - give max rew value (1)
                print(self.bilard.closest_ball.is_hit)
                if self.bilard.closest_ball.is_hit:
                    print("bila trafiona")
                    rew_2 = 1
                else:
                    d_end_rew_2 = self.bilard.d_rew_2()
                    rew_2 = self.bilard.calculate_rew_2(d_start_rew_2, d_end_rew_2)

                # CALCULATE REWARD 3 FROM SAVED_VELOCITY OF CHOSEN BALL
                rew_3 = 0
                rew_4 = 0
                aim_point = 0, 0
                if self.bilard.closest_ball.saved_velocity is not None and (self.bilard.closest_ball.saved_velocity[0] != 0 or self.bilard.closest_ball.saved_velocity[1]!=0):
                    position = self.bilard.closest_ball.saved_position
                    velocity = self.bilard.closest_ball.saved_velocity * (-1)

                    print(position, velocity)

                    vec = Vector(position, position + velocity)
                    aim_point = intersect(vec, table)
                    print(f'aim point: {aim_point}')

                    chosen_hole, min_dist = closest_hole(aim_point, all_holes)

                    d_start_rew_3 = self.bilard.dist_from_hole(position, chosen_hole)
                    d_end_rew_3   = self.bilard.dist_from_hole(self.bilard.closest_ball.body.position, chosen_hole)

                    if self.bilard.closest_ball.is_in_hole:
                        rew_3 = 1
                    else:
                        rew_3 = self.bilard.calculate_rew_2(d_start_rew_3, d_end_rew_3)

                    position = None
                    velocity = None
                    vec = None
                    aim_point = None

                    rew_4 = min(1, 60/min_dist)
                


                """
                for i in range(500):
                    # self.pygame.pymunk_space.step(1)
                    #self.render(action)
                    pygame.draw.circle(self.bilard.pygame_screen, RED, convert_coordinates(chosen_hole.center), 20)
                    pygame.draw.circle(self.bilard.pygame_screen, YELLOW, convert_coordinates(aim_point), 20)
                    pygame.display.flip()
                """

                # add reward to final score
                self.bilard.finish_score += rew_1
                #self.bilard.finish_score += max(-1/2, rew_1_1)
                self.bilard.finish_score += max(-1/2, rew_1 * rew_2)
                self.bilard.finish_score += rew_3
                #self.bilard.finish_score += max(-1/2, rew_1 * rew_4)

                print(f'rew_1  : {rew_1}')
                print(f'rew_1_1: {rew_1_1}')
                print(f'rew_2  : {rew_2}')
                print(f'rew_3  : {rew_3}')
                print(f'rew_4  : {rew_4}')

                # OBS, REWARD AND CHECKING IF GAME HAS ENDED
                obs = self.bilard.observe()
                reward = self.bilard.evaluate(action, obs)
                print(f"\nreward: {reward}\n")
                done = self.bilard.is_done(1)

                return obs, reward, done, {}

    def render(self, action, mode="human", close=False):
        if self.bilard.show_game:
            pygame.event.pump()  # this makes pygame window work properly
            self.bilard.draw()
            pygame.draw.circle(self.bilard.pygame_screen, (24, 254, 0),
                               convert_coordinates(((action[0]+1)/2 * SCREEN_WIDTH, (action[1]+1)/2 * SCREEN_LENGTH)), 10, True,
                               False, False, False)

            pygame.display.flip()
