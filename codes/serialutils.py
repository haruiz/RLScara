import serial
import time


if __name__ == '__main__':
    arduino = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 1)
    time.sleep(2)
    

    arduino.write(b'65,180')
    


    line = arduino.readline()
    

    print(line.decode('utf-8'))
    

    arduino.close()
        