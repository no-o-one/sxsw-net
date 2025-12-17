'''the RYLR driver uses machine.UART module which is not for standard python. this wrapper class to makes it so the RYLR998 driver is compatible with the pyserial module that is used instead

used in src/utils to init the lora module'''

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
