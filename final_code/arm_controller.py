import typing

from arduino_utils import SerialPort


class ArmController:
    """A class that controls the 3D printed arm using arduino."""

    def __init__(
        self,
        port: str = SerialPort.default,
        baudrate=9600,
        timeout: typing.Union[int, float] = 1,
    ):
        """
        Initializes the arm controller.
        :param port: The serial port to use.
        :param baudrate: The baudrate to use.
        :param timeout: The timeout to use.
        """
        self.port = SerialPort(port, baudrate, timeout)

    def move_to(self, *angles: int):
        """
        Moves the arm to the specified location defined by the angles.
        :param angles:
        :return:
        """
        self.port.write(",".join(map(str, angles)))
        line = self.port.readline()
        print(line)

    def is_connected(self) -> bool:
        """
        Returns true if the arm controller is connected.
        :return:
        """
        # we basically just check if we can connect to the arduino
        return self.port.is_open()

    def reset(self):
        """
        Resets the arm controller to the initial position.
        :return:
        """
        self.port.write("0,90")
        line = self.port.readline()
        print(line)

    def __enter__(self):
        self.port.open()  # open the serial port connection
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.port.close()  # close the serial port connection


if __name__ == "__main__":
    with ArmController() as arm_controller:
        if arm_controller.is_connected():
            arm_controller.reset()
            arm_controller.move_to(90, 180)
