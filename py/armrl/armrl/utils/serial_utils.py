import serial
import time
import serial.tools.list_ports


class SerialPort:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(2)

    @classmethod
    @property
    def default(cls):
        """
        Returns the default serial port.
        """
        return cls.available_ports()[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ser.close()

    def readline(self):
        """
        Reads a line from the serial port.
        """
        return self.ser.readline().decode("utf-8")

    def write(self, data):
        """
        Writes data to the serial port.
        """
        self.ser.write(bytes(data, "utf-8"))

    def read(self, size):
        """
        Reads data from the serial port.
        """
        return self.ser.read(size).decode("utf-8")

    @classmethod
    def available_ports(cls):
        """
        Returns a list of available serial ports
        """
        return [port.device for port in serial.tools.list_ports.grep("USB")]


if __name__ == "__main__":
    with SerialPort(port=SerialPort.default, baudrate=9600, timeout=1) as arduino:
        arduino.write("90,90")
        line = arduino.readline()
        print(line)
