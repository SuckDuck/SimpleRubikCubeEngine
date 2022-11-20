import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import enviroment

rubik_cube = enviroment.rubik_env()

def create_model(cubo,actions):
    model = Sequential()
    model.add(Flatten(input_shape=(3,3,3,6)))
    model.add(Dense(100,activation="relu"))
    model.add(Dense(100,activation="relu"))
    model.add(Dense(50,activation="relu"))
    model.add(Dense(50,activation="relu"))
    model.add(Dense(25,activation="relu"))
    model.add(Dense(25,activation="relu"))
    model.add(Dense(12,activation="linear"))
    return model

def create_agent(model,actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=500000,window_length=1)
    dqn = DQNAgent(model=model,memory=memory,policy=policy,nb_actions=actions,nb_steps_warmup=0,target_model_update=0.01)
    return dqn

model = create_model(rubik_cube.cube.cube,rubik_cube.action_space.n)
dqn = create_agent(model,rubik_cube.action_space.n)

dqn.compile(Adam(lr=0.001),metrics=["mae"])
dqn.fit(rubik_cube,nb_steps=50000,visualize=False,verbose=1)
#dqn.save_weights("rubik_cube_model.h5f",overwrite=True)