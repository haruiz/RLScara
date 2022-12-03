from urdfpy import URDF
import numpy as np

robot = URDF.load('urdfs/urdf/assembly.SLDASM.urdf')
for joint in robot.actuated_joints:
    print(joint.name)
fk = robot.link_fk()

robot.animate(cfg_trajectory={'joint1': [-np.pi / 2, np.pi / 2],'joint2': [-np.pi / 2, np.pi / 2]})