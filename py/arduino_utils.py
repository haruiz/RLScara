import typing

import serial
import time
import serial.tools.list_ports


class SerialPort:
    """A class to send and receive data over a serial port."""

    def __init__(self, port: str, baudrate: int, timeout: typing.Union[int, float]):
        """
        Initializes the serial port.
        :param port: The serial port to use.
        :param baudrate: The baudrate to use.
        :param timeout: The timeout to use.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

    @classmethod
    @property
    def default(cls) -> str:
        """
        Returns the default serial port.
        """
        available_ports = cls.available_ports()
        return available_ports[0] if len(available_ports) > 0 else None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        """
        Opens the serial port.
        """
        if not self.is_open():
            self.ser.open()
        time.sleep(2)

    def close(self):
        """
        Closes the serial port.
        """
        self.ser.close()

    def readline(self) -> str:
        """
        Reads a line from the serial port.
        """
        return self.ser.readline().decode("utf-8")

    def write(self, data: str):
        """
        Writes data to the serial port.
        :param data: The data to write to the serial port.
        :return:
        """
        self.ser.write(bytes(data, "utf-8"))

    def read(self, size: int) -> str:
        """
        Reads data from the serial port.
        :param size: The number of bytes to read from the serial port.
        :return:
        """
        return self.ser.read(size).decode("utf-8")

    @classmethod
    def available_ports(cls) -> typing.List[str]:
        """
        Returns a list of available serial ports
        """
        available_ports = [port.device for port in serial.tools.list_ports.grep("USB")]
        return available_ports

    @classmethod
    def is_available(cls, port: str) -> bool:
        """
        Returns true if the specified port is available.
        """
        return port in cls.available_ports()

    def is_open(self) -> bool:
        """
        Returns true if the serial port is open.
        """
        return self.ser is not None and self.ser.isOpen()


if __name__ == "__main__":
    print(SerialPort.available_ports())
    with SerialPort("/dev/cu.usbmodem141112401", 9600, 1) as port:
        if port.is_open():
            port.write("90,90")
            print(port.readline())
