import pyglet

from arm_env import Arm, ArmSimViewer
from arm_rl_model import DDPG
from color_utils import ColorUtils
from math_utils import *
from plot_utils import plot_episode_stats
import random
import typer

# ****** parameters ******#
ENV_SIZE = Size2D(300, 300)
ARM_ORIGIN = Point2D(ENV_SIZE.width / 2, 0)
N_LINKS = 2
LINK_LENGTH = 100
MAX_EPISODES = 900
MAX_EP_STEPS = 300


# ****** arm setup ******#
env = Arm(ARM_ORIGIN, env_size=ENV_SIZE, link_width=10)
colors_dict = ColorUtils.rainbow(n=N_LINKS)
R = colors_dict["r"]
G = colors_dict["g"]
B = colors_dict["b"]
rainbow_colors = list(zip(B, G, R))
for i in range(N_LINKS):
    env.add_link(LINK_LENGTH, rainbow_colors[i])
env.set_angles(*len(env.links) * [0])

# ****** model setup ******#
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound
rl_model = DDPG(a_dim, s_dim, a_bound)


app = typer.Typer()


@app.command()
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
    plot_episode_stats(
        steps_list,
        reward_values,
        title=f"DDPG on Arm Environment: N-links {len(env.links)}, Env Size: {ENV_SIZE.width} * {ENV_SIZE.height}",
        output_file=f"plots/n_links_{len(env.links)}_env_size_{ENV_SIZE.width}X{ENV_SIZE.height}.png"
    )


@app.command()
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


@app.command()
def render():
    """
    Renders the environment using the pyglet based viewer.
    """
    rl_model.restore()
    ArmSimViewer(env, rl_model, ENV_SIZE)
    pyglet.app.run()

@app.command()
def sim():

    ENV_SIZE = Size2D(600, 600)
    ARM_ORIGIN = Point2D(ENV_SIZE.width / 2, 0)
    N_LINKS = 10
    LINK_LENGTH = 40

    env = Arm(ARM_ORIGIN, env_size=ENV_SIZE, link_width=10)
    colors_dict = ColorUtils.rainbow(n=N_LINKS)
    R = colors_dict["r"]
    G = colors_dict["g"]
    B = colors_dict["b"]
    rainbow_colors = list(zip(B, G, R))
    for i in range(N_LINKS):
        env.add_link(LINK_LENGTH, rainbow_colors[i])
    env.set_angles(*len(env.links) * [0])

    ArmSimViewer(arm=env, env_size=ENV_SIZE, model=None)
    env.set_angles(90,45,45,180,90,180,45,45,180,90)
    pyglet.app.run()


if __name__ == "__main__":
    app()
