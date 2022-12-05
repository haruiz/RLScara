from arm_env import Arm, ArmSimViewer
from math_utils import *

# helpers
from arm_rl_model import DDPG
from plot_utils import plot_episode_stats
import pyglet

ON_TRAIN = False

# set env
env_size = Size2D(300, 300)  # max spawn of the arm
arm_origin = Point2D(env_size.width / 2, 0)

# set arm
env = Arm(arm_origin, env_size=env_size, link_width=10)
env.add_link(100, (255, 0, 0))
env.add_link(100, (0, 255, 0))


# set model
MAX_EPISODES = 900
MAX_EP_STEPS = 200
# get model params from th environment
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound
rl_model = DDPG(a_dim, s_dim, a_bound)

steps = []


def train():
    """This function performs the training of the model"""
    reward_values = []
    steps_list = []
    for i in range(MAX_EPISODES):
        s = env.reset()
        ep_r = 0.0
        for j in range(MAX_EP_STEPS):
            a = rl_model.choose_action(s)
            s_, r, done = env.step(a)
            rl_model.store_transition(s, a, r, s_)

            ep_r += r
            if rl_model.memory_full:
                # start to learn once has fulfilled the memory
                rl_model.learn()
            s = s_
            if done or j == MAX_EP_STEPS - 1:
                print(
                    "Ep: %i | %s | ep_r: %.1f | step: %i"
                    % (i, "---" if not done else "done", ep_r, j)
                )
                reward_values.append(ep_r)
                steps_list.append(j)
                break

    rl_model.save()
    plot_episode_stats(steps_list, reward_values)


def eval():
    """This function performs the evaluation of the model"""

    rl_model.restore()
    s = env.reset()
    tolerance_counter = 0
    tolerance = 0.001
    prevr = 0

    while True:
        a = rl_model.choose_action(s)
        s, r, done = env.step(a)

        if abs(r - prevr) < tolerance:
            tolerance_counter += 1
        else:
            tolerance_counter = 0

        prevr = r
        if done or tolerance_counter > 10:  # check if reached or saturated
            print("reward:", r)
            for i, link in enumerate(env.links):
                print("angle of link ", i, rad2deg(link.angle))
            break


def render():
    """
    Renders the environment using the pyglet based viewer.
    """
    rl_model.restore()
    ArmSimViewer(env, rl_model, env_size)
    pyglet.app.run()


if __name__ == '__main__':
    if ON_TRAIN:
        train()
    else:
        render()
