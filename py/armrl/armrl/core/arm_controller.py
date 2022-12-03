from armrl.utils import SerialPort


class ArmController:
    def __init__(self, port=SerialPort.default, baudrate=9600, timeout=1):
        self.port = SerialPort(port, baudrate, timeout)

    def move(self, *angles):
        """
        Moves the arm to the specified location defined by the angles.
        :param angles:
        :return:
        """
        self.port.write(",".join(map(str, angles)))
        line = self.port.readline()
        print(line)


if __name__ == "__main__":
    arm_controller = ArmController()
    # move to 90 degrees for the first servo and 180 degrees for the second servo
    arm_controller.move(90, 180)
