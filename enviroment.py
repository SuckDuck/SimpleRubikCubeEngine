from gym import Env
from gym.spaces import Discrete
import engine

class rubik_env(Env):
    def __init__(self) -> None:
        #super().__init__()
        self.cube = engine.cube()
        self.action_space = Discrete(12)
        self.max_movements = 500
    
    def step(self,action):

        if action == 0: action = "R"
        if action == 1: action = "Ri"
        if action == 2: action = "L"
        if action == 3: action = "Li"
        if action == 4: action = "B"
        if action == 5: action = "Bi"
        if action == 6: action = "D"
        if action == 7: action = "Di"
        if action == 8: action = "F"
        if action == 9: action = "Fi"
        if action == 10: action = "U"
        if action == 11: action = "Ui"

        self.cube.turn_face(action)
        self.max_movements -= 1

        state = self.cube.cube
        reward = self.cube.get_reward()
        if reward == 27 or self.max_movements <= 0:
            done = True
        else: done = False
        info = {}

        return state, reward, done, info

    def render(self):
        self.cube.show_cube(save=True)

    def reset(self):
        self.cube.reset()
        self.max_movements = 500
        return self.cube

"""rubik_cube = rubik_env()

score = 0
done = False
state = rubik_cube.reset()
rubik_cube.cube.scramble_cube()
while not done:
    rubik_cube.render()
    action = rubik_cube.action_space.sample()
    state, reward, done, info = rubik_cube.step(action)
print(reward)"""
