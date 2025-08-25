"""
Lightweight driver for interfacing with the RYLR998 LoRa module by REYAX.
Author Tim Hanewich, github.com/TimHanewich
Find updates to this code: https://github.com/TimHanewich/MicroPython-Collection/blob/master/REYAX-RYLR998/

MIT License
Copyright 2024 Tim Hanewich
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

this file has been fully reworked
"""

import machine
import time
import ubinascii

class ReceivedMessage:
    def __init__(self):
        self.address = None
        self.length = None
        self.data = None
        self.RSSI = None
        self.SNR = None

    def parse(self, full_line: bytes):
        try:
            parts = full_line.decode("ascii").strip().split(",")
            header, address = parts[0].split("=")
            self.address = int(address)
            self.length = int(parts[1])
            self.data = parts[2].encode("ascii")  # leave as bytes
            self.RSSI = int(parts[3])
            self.SNR = int(parts[4])
        except Exception as e:
            raise Exception(f"Failed to parse message: {full_line} => {e}")

    def __str__(self):
        return f"From {self.address}, RSSI={self.RSSI}, SNR={self.SNR}, Data={self.data}"


class RYLR998:
    def __init__(self, uart: machine.UART):
        self._uart = uart
        self._rxbuf = b''
        self._pending_cmd = None
        self._pending_cmd_start = 0
        self._pending_cmd_timeout = 0
        self._last_send_status = None

        while self._uart.any():
            self._uart.read()

    def send_blocking(self, address: int, data: bytes):
        if len(data) > 240:
            raise ValueError("Data too long (>240 bytes)")

        cmd = b"AT+SEND=%d,%d," % (address, len(data)) + data + b"\r\n"
        self._uart.write(cmd)
        resp = self._wait_for_response(8000)
        if resp != b"+OK\r\n":
            raise Exception(f"Send failed: {resp}")

    def send(self, address: int, data: bytes): #MAKE SURE TO CHECK SEND STATUS BEFORE SENDING ANOTHER MESSAGE, THIS IS CRUCIAL
        """Start sending data, and return immediately. Use check_send_status() to complete."""
        if len(data) > 240:
            raise ValueError("Data too long (>240 bytes)")
        cmd = b"AT+SEND=%d,%d," % (address, len(data)) + data + b"\r\n"
        self._uart.write(cmd)
        self._pending_cmd = "send"
        self._pending_cmd_start = time.ticks_ms()
        self._pending_cmd_timeout = 8000
        self._last_send_status = None

    def check_send_status(self):
        """Returns True if +OK received, False if still waiting, raises if failed."""
        if self._last_send_status is not None:
            return self._last_send_status

        self._collect_rx()
        if self._uart.any():
            data = self._uart.read()
            if data.startswith(b"+OK"):
                self._last_send_status = True
                self._pending_cmd = None
                return True
            elif data.startswith(b"+RCV"):
                self._rxbuf += data
            else:
                raise Exception(f"Unexpected response: {data}")
        if time.ticks_diff(time.ticks_ms(), self._pending_cmd_start) > self._pending_cmd_timeout:
            self._pending_cmd = None
            raise TimeoutError("Send confirmation not received")
        return False

    def receive(self):
        """Returns ReceivedMessage if available, otherwise None. Non-blocking."""
        self._collect_rx()
        start = self._rxbuf.find(b"+RCV=")
        if start == -1:
            return None
        end = self._rxbuf.find(b"\r\n", start)
        if end == -1:
            return None  # Not complete yet
        msg_line = self._rxbuf[start:end+2]
        self._rxbuf = self._rxbuf[:start] + self._rxbuf[end+2:]
        msg = ReceivedMessage()
        msg.parse(msg_line)
        return msg

    def _collect_rx(self):
        data = self._uart.read()
        if data:
            self._rxbuf += data

    def _wait_for_response(self, timeout_ms):
        self._collect_rx()
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
            if self._uart.any():
                data = self._uart.read()
                if data.startswith(b"+RCV"):
                    self._rxbuf += data
                else:
                    return data
            time.sleep_ms(1)
        raise TimeoutError("No response received in time")

    def pulse(self):
        self._uart.write(b"AT\r\n")
        try:
            resp = self._wait_for_response(1000)
            return resp == b"+OK\r\n"
        except:
            return False

    def address(self):
        self._uart.write(b"AT+ADDRESS?\r\n")
        resp = self._wait_for_response(1000)
        return int(resp.decode().strip().split("=")[1])

    def set_address(self, addr: int):
        cmd = b"AT+ADDRESS=" + str(addr).encode() + b"\r\n"
        self._uart.write(cmd)
        resp = self._wait_for_response(1000)
        if resp != b"+OK\r\n":
            raise Exception(f"Set address failed: {resp}")

    def software_reset(self):
        self._uart.write(b"AT+RESET\r\n")
        start = time.ticks_ms()
        expected = b"+RESET\r\n+READY\r\n"
        collected = b""
        while time.ticks_diff(time.ticks_ms(), start) < 5000:
            if self._uart.any():
                collected += self._uart.read()
                if collected == expected:
                    return
        raise TimeoutError("Reset not confirmed")

def safe_reyax_connection_setup(id, max_retries=5):
    import time
    from src import reyax
    for i in range(max_retries):
        try:
            print(f"> LoRa setup try {i+1}")
            rylr = reyax.connection_setup(id)
            print("> LoRa setup succeeded")
            return rylr
        except Exception as e:
            print(f"! LoRa setup failed: {e}")
            time.sleep(1)
    raise RuntimeError("LoRa module not responding")



def connection_setup(self_address: int) -> RYLR998:
    uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))
    rylr = RYLR998(uart)
    rylr.set_address(self_address)
    if not rylr.pulse():
        print("WARNING: LoRa module test failed.")
    print(f"> Connected module address: {self_address}")
    msg = f"> Module #{self_address} online".encode()
    rylr.send(65335, msg)
    return rylr

