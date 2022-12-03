from armrl.core import ArmController

if __name__ == '__main__':
    arm_controller = ArmController()
    # move to 90 degrees for the first servo and 180 degrees for the second servo
    arm_controller.move(90, 90)