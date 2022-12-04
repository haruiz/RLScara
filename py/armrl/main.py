from armrl.core import ArmController
import numpy as np

if __name__ == "__main__":
    arm_controller = ArmController()
    # move to 90 degrees for the first servo and 180 degrees for the second servo
    for angle in np.arange(0, 180, 10):
        arm_controller.move(angle, 90)
