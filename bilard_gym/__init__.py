from gym.envs.registration import register

register(
    id='Bilard-v0',
    entry_point='bilard_gym.envs:BilardEnv',
)