from typing import *
import numpy as np
import random
import gymnasium as gym
import time
from threading import Lock
from torch.cuda import is_available

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv

from checkpoint import Checkpoint
from checkpointmanager import CheckpointManager, checkpoints

from controller import Supervisor
S = Supervisor()

import torch.nn as nn

import os
import sys

# this is necessary because we are not in a package context
# so we cannot do from ..config import *
# SO EVEN IF IT LOOKS UGLY, WE HAVE TO DO THIS
script_dir = os.path.dirname(os.path.abspath(__file__))
controllers_path = os.path.join(script_dir, '../../controllers')
sys.path.append(controllers_path)

from config import *
from extractor import CNN1DExtractor


import matplotlib.pyplot as plt
#plt.ion()
# fig, ax = plt.subplots()
# line, = ax.plot([], [])
# plt.xlim(-lidar_max_range, lidar_max_range)
# plt.ylim(-lidar_max_range, lidar_max_range)
# plt.scatter(0, 0, c="red", marker="+")



class WebotsGymEnvironment(gym.Env):
    """
    One environment for each vehicle

    n: index of the vehicle
    supervisor: the supervisor of the simulation
    """

    def __init__(self, i: int, n_envs: int, n_actions: int, n_sensor: int, lidar_horizontal_resolution: int, lidar_max_range: float, reset_lock: Lock):
        #print the exported node string
        print("BEGINS INIT")
        self.i = i
        if n_envs <= 1:
            self.y = -2.5
        else:
            self.y = -2.5 + (self.i / (n_envs - 1) - 0.5) * 1.2
        self.n_actions = n_actions

        self.lidar_horizontal_resolution = lidar_horizontal_resolution
        self.lidar_max_range = lidar_max_range
        self.n_sensors = n_sensor

        self.checkpoint_manager = CheckpointManager(S, checkpoints)

        basicTimeStep = int(S.getBasicTimeStep())
        print(f"{basicTimeStep=}")
        self.sensorTime = basicTimeStep // 4

        self.reset_lock = reset_lock
        # virtual time of the last reset

        # negative value so that the first reset is not skipped
        self.last_reset = -1e6
        #print(f"{self.last_reset=}")

        # Emitter
        self.emitter = S.getDevice(f"supervisor_emitter_{i}")
        self.emitter.setChannel(2 * self.i)

        # Receiver
        self.receiver = S.getDevice(f"supervisor_receiver_{i}")
        self.receiver.enable(self.sensorTime)
        self.receiver.setChannel(2 * self.i + 1)

        # Last data received from the car
        self.last_data = np.zeros(self.lidar_horizontal_resolution + self.n_sensors, dtype=np.float32)

        self.translation_field = S.getFromDef(f"TT02_{self.i}").getField("translation") # may cause access issues ...
        self.rotation_field = S.getFromDef(f"TT02_{self.i}").getField("rotation") # may cause access issues ...

        self.action_space = gym.spaces.Discrete(n_actions) #actions disponibles
        box_min = np.zeros(self.n_sensors + self.lidar_horizontal_resolution)
        box_max = np.ones(self.n_sensors + self.lidar_horizontal_resolution)
        self.observation_space = gym.spaces.Box(box_min, box_max, dtype=np.float32) #Etat venant du LIDAR
        print(self.observation_space)
        print(self.observation_space.shape)

        print("try to reset the environment",  self.i)
        self.reset()

    # returns the lidar data of all vehicles
    def observe(self):
        # gets from Receiver
        if self.receiver.getQueueLength() > 0:
            while self.receiver.getQueueLength() > 1:
                self.receiver.nextPacket()
            self.last_data = np.clip(np.frombuffer(self.receiver.getBytes(), dtype=np.float32), 0, self.lidar_max_range)

        # if self.i == 0:
        #     deadzone = np.pwzi/2
        #     angle = -(2 * np.pi - deadzone) * np.arange(self.lidar_horizontal_resolution) / self.lidar_horizontal_resolution - deadzone/2 + np.pi/2
        #     line.set_xdata(np.cos(angle) * self.last_data[self.n_sensors:])
        #     line.set_ydata(np.sin(angle) * self.last_data[self.n_sensors:])

        #     plt.draw()
        #     plt.pause(0.01)
        return self.last_data

    # reset the gym environment reset
    def reset(self, seed=0):
        global n_envs

        # this has to be done otherwise thec cars will shiver for a while sometimes when respawning and idk why
        if S.getTime() - self.last_reset >= 1:
            #print(self.last_reset, S.getTime() - self.last_reset)
            self.last_reset = S.getTime()

            self.checkpoint_manager.reset()

            INITIAL_trans = [-1, self.y, 0.0391]
            INITIAL_rot = [-0.304369, -0.952554, -8.76035e-05 , 6.97858e-06]

            # WARNING: this is not thread safe
            # This may not be necessary but it's better to be safe than sorry
            # with self.reset_lock:
            vehicle = S.getFromDef(f"TT02_{self.i}")
            self.translation_field.setSFVec3f(INITIAL_trans)
            self.rotation_field.setSFRotation(INITIAL_rot)
            vehicle.resetPhysics()

        obs = self.observe()
        #super().step()
        info = {}
        return obs, info

    # step function of the gym environment
    def step(self, action):
        #print("Action: ", action)
        steeringAngle = np.linspace(-.44, .44, self.n_actions, dtype=np.float32)[action, None]
        self.emitter.send(steeringAngle.tobytes())

        # we should add a beacon sensor pointing upwards to detect the beacon
        obs = self.observe()
        sensor_data = obs[:self.n_sensors]

        reward = 0
        done = False
        truncated = False

        x, y, _ = self.translation_field.getSFVec3f()
        b_past_checkpoint = self.checkpoint_manager.update(x, y)

        b_collided, = sensor_data # unpack sensor data
        # print(f"data received from car {self.i}", obs[:6])

        if b_collided:
            reward = -250
            done = True
        elif b_past_checkpoint:
            reward = 100 * np.cos(self.checkpoint_manager.get_angle() - self.rotation_field.getSFRotation()[3])
            done = False
            print(f"reward: {reward}")
        else:
            reward = 1
            done = False

        S.step()

        return obs, reward, done, truncated, {}

    #Fonction render de l"environnement GYM
    def render(self, mode="human", close=False):
        pass



#----------------Programme principal--------------------
def main():
    print("Creating environment")

    # global i
    # i = -1
    # def f():
    #     global i
    #     i += 1
    #     return WebotsGymEnvironment(i, lidar_horizontal_resolution)
    # env = make_vec_env(
    #     f,
    #     n_envs=n_envs,
    #     vec_env_cls=SubprocVecEnv
    # )

    reset_lock = Lock()
    env = DummyVecEnv([lambda i=i: WebotsGymEnvironment(i, n_envs, n_actions, n_sensor, lidar_horizontal_resolution, lidar_max_range, reset_lock) for i in range(n_envs)])

    print("Environment created")
    # check_env(env)

    logdir = "./Webots_tb/"
    #-- , tensorboard_log = logdir -- , tb_log_name = "PPO_voiture_webots"

    policy_kwargs = dict(
        features_extractor_class=CNN1DExtractor,
        features_extractor_kwargs=dict(
            n_sensors=n_sensor,
            lidar_horizontal_resolution=lidar_horizontal_resolution,
            device="cuda" if is_available() else "cpu"
        ),
        activation_fn=nn.ReLU,
    )

    gamma = 0.5**(S.getBasicTimeStep() * 1e-3 / 5)
    gamma = .975
    print(f"{gamma=}")
    #Définition modèle avec paramètre par défaut
    model = PPO("MlpPolicy", env,
        n_steps=2048,
        n_epochs=10,
        batch_size=64,
        learning_rate=3e-3,
        gamma=gamma, # calculated so that discounts by 1/2 every T seconds
        verbose=1,
        device="cuda" if is_available() else "cpu",
        policy_kwargs=policy_kwargs
    )

    print(model.policy)
    print("are features_extractors the same?",
        model.policy.vf_features_extractor is
        model.policy.features_extractor is
        model.policy.pi_features_extractor
    )
    print("are mlp_extractors the same?",
        model.policy.mlp_extractor.policy_net == model.policy.mlp_extractor.value_net
    )


    #Entrainnement
    model.learn(total_timesteps=1e6)

    #Sauvegarde
    model.save("Voiture_autonome_Webots_PPO")

    #del model

    #Chargement des données d"apprentissage
    model = PPO.load("Voiture_autonome_Webots_PPO")

    obs = env.reset()

    for _ in range(1000000):
        #Prédiction pour séléctionner une action à partir de l"observation
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        if done:
            obs = env.reset()


if __name__ == "__main__":
    main()
