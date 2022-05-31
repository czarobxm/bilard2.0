from cgitb import reset
import gym
import bilard_gym
import numpy as np
from stable_baselines3.common.noise import NormalActionNoise

import pygame
import os

import tensorboard

from stable_baselines3 import SAC, PPO, A2C, TD3


# saving paths
models_dir = f"models/PPO"
log_dir = f"logs/PPO"
model_path = f"{models_dir}/244"


# creating directories for models and logs
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# making environment
env = gym.make('Bilard-v0')
env.reset()

iter = [1,2,3]
cr_list = [0.05, 0.1, 0.15]
tb_log_name = "PPO_REWARD_3_test_"
log_list = [f'{tb_log_name}33', f'{tb_log_name}34', f'{tb_log_name}35']

#for cr, log, i in zip(cr_list, log_list, iter):
# creating and loading model
model = TD3("MlpPolicy",
            env,
            verbose=2,
            tensorboard_log=log_dir,
            #learning_starts=3000,
            action_noise=NormalActionNoise(mean=np.zeros(3), sigma=np.array([0.008, 0.008, 0.1])),
            #n_steps=640 * 2,

            learning_rate=0.0003,
            #clip_range_vf=0.1,
            )
            #clip_range=0.2)

#model = model.load(model_path, env=env)

# Learning process
episodes = 125000
TIMESTEPS = 2


for i in range(1, episodes):
    print(f'{i} ' * 100)

    model.learn(total_timesteps=TIMESTEPS,
                reset_num_timesteps=False,
                tb_log_name=f'{tb_log_name}55')

    model.save(f"{models_dir}/{TIMESTEPS * i}")

obs = env.reset()

print("PREZENTACJA MODELU:")
for i in range(25):
    print(F"PREZENTACJA NR {i + 1}")
    env.render()
    action, _states = model.predict(obs, deterministic=False)
    print(action)
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()

env.close()

