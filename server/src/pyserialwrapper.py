#this is a wrapper class to make the RYLR998 driver compatible with the pyserial mudule
#it is neede due to the fact that the driver uses machine.UART module instead which is not available on python
import serial

class pyserialUARTwrapper:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.serial = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.baudrate = baudrate

    def write(self, data):
        return self.serial.write(data)

    def read(self, size=1):
        return self.serial.read_all()

    def any(self):
        return self.serial.in_waiting

    def init(self, baudrate):
        self.serial.baudrate = baudrate
        self.baudrate = baudrate

    def close(self):
        self.serial.close()
