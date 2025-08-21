import serial
import time


def pack_5_octal_digits(d0, d1, d2, d3, d4) -> bytes:
    """Pack 5 octal digits (0–7 each) into exactly 2 bytes (15 bits)."""
    digits = [d0, d1, d2, d3, d4]
    bits = 0
    for digit in digits:
        if not (0 <= digit <= 7):
            raise ValueError("Each digit must be between 0 and 7")
        bits = (bits << 3) | digit
    return bits.to_bytes(2, 'big')


def unpack_5_octal_digits(packed: bytes) -> list:
    """Unpack 2 bytes into 5 octal digits."""
    if len(packed) != 2:
        raise ValueError("Packed data must be exactly 2 bytes")
    bits = int.from_bytes(packed, 'big') & 0x7FFF
    return [(bits >> shift) & 0b111 for shift in range(12, -1, -3)]


class RYLR998SerialDriver:
    def __init__(self, port: str, baudrate: int = 115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Allow the serial port to stabilize

    def send(self, address: int, data):
        """Send either an ASCII string or a list of 5 octal digits (integers 0–7)."""
        if isinstance(data, str):
            payload = data.encode("ascii")
            print(f"> Sending ASCII message: {data}")
        elif isinstance(data, list) and len(data) == 5:
            payload = pack_5_octal_digits(*data)
            print(f"> Sending raw octal data: {data} -> {payload}")
        else:
            raise ValueError("Data must be a string or a list of 5 octal digits (0–7).")

        command = f"AT+SEND={address},{len(payload)},".encode("ascii") + payload + b"\r\n"
        self.ser.write(command)
        print(f"> Command sent: {command}")

    def read_response(self):
        """Read and print any responses from the module."""
        while self.ser.in_waiting:
            line = self.ser.readline()
            if line:
                print(f"< {line.strip()}")

    def close(self):
        self.ser.close()





if __name__ == "__main__":
    driver = RYLR998SerialDriver("COM14")  # Change to your actual serial port
    target_address = 1234

    # Send ASCII message
    #driver.send(target_address, "Hello LoRa!")

    # Send 5-digit octal as raw data
    #driver.send(target_address, [1, 0, 3, 7, 4])

    # Read any responses
    time.sleep(1)
    driver.read_response()

    #driver.close()
