from urdfpy import URDF
import numpy as np

robot = URDF.load('urdfs/urdf/assembly.SLDASM.urdf')
for joint in robot.actuated_joints:
    print(joint.origin)

for link in robot.links:
    print(link.name)
robot.animate(cfg_trajectory={'joint1': [-np.pi / 2, np.pi / 2],'joint2': [-np.pi / 2, np.pi / 2]})