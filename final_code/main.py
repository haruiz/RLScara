from arm_env import Arm, Point2D, ArmSimViewer
# helpers
from arm_env import rad2deg, deg2rad
from rl import DDPG
import pyglet

MAX_EPISODES = 900
MAX_EP_STEPS = 200
ON_TRAIN = False

# set env
env_size = Point2D(200,200) # max spawn of the arm
arm_origin = Point2D(0, env_size.y/2)

env = Arm(arm_origin, env_size = env_size, link_width=20)
env.add_link(100,(255, 0, 0))
env.add_link(100,(0, 255, 0))
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

# set RL method (continuous)
rl = DDPG(a_dim, s_dim, a_bound)


steps = []
def train():
    # start training
    for i in range(MAX_EPISODES):
        s = env.reset()
        ep_r = 0.
        for j in range(MAX_EP_STEPS):
            # env.render()

            a = rl.choose_action(s)

            s_, r, done = env.step(a)

            rl.store_transition(s, a, r, s_)

            ep_r += r
            if rl.memory_full:
                # start to learn once has fulfilled the memory
                rl.learn()

            s = s_
            if done or j == MAX_EP_STEPS-1:
                print('Ep: %i | %s | ep_r: %.1f | step: %i' % (i, '---' if not done else 'done', ep_r, j))
                break
    rl.save()


def eval():
    rl.restore()
    #env.render()
    #env.viewer.set_vsync(True)
    s = env.reset()
    tolerance_counter = 0
    tolerance = 0.001
    prevr = 0
    while True:
        #env.render()
        a = rl.choose_action(s)
        s, r, done = env.step(a)

        if(abs(r-prevr)<tolerance):
            tolerance_counter += 1
        else:
            tolerance_counter = 0

        prevr = r
        
        if done or tolerance_counter>10:    # check if reached or saturated
            print('reward:',r)
            for i, link in enumerate(env.links):
                print('angle of link ',i,rad2deg(link.angle))
            break


def onmouseViewer():
    rl.restore()
    viewer = ArmSimViewer(env,rl)
    pyglet.app.run()

if ON_TRAIN:
    train()
else:
    onmouseViewer()



