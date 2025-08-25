import time
import src.pyserialwrapper as pyserialwrapper
import src.reyax as reyax
from src.Mesh import *


#LORA MODULE SETUP
port = '/dev/tty.usbserial-XX' #placeholder
baudrate = 115200
try:
    uart = pyserialwrapper.pyserialUARTwrapper(port, baudrate)
    rylr = reyax.RYLR998(uart)
    rylr.address = 65535
    if not rylr.pulse:
        print('!WARNING! LoRa module test failed')
except Exception as e:
    print(f'!WARNING! Connection to LoRa at {port} with baudrate {baudrate} failed with the following: \n{e}')

#setup existing mesh of nodes
thismesh = Mesh([[1,2,3]])


def pack_octal(d0, d1, d2, d3, d4) -> bytes:
    """Packs 5 octal digits (0–7 each) into exactly 2 bytes (15 bits).
    all digits MUST be 0-7, so it must be an octal number"""
    digits = [d0, d1, d2, d3, d4]
    bits = 0
    for digit in digits:
        bits = (bits << 3) | digit  # shift left 3 bits, OR in the digit
    return bits.to_bytes(2, 'big')  # 2-byte big-endian representation


def unpack_octal(packed: bytes) -> list:
    """Unpacks 2 bytes into a list of 5 octal digits (as integers)."""
    if len(packed) != 2:
        return []

    bits = int.from_bytes(packed, 'big') & 0x7FFF  # 15 bits mask
    digits = []
    for shift in range(12, -1, -3):
        digits.append((bits >> shift) & 0b111)
    return digits



def ping(id_to_ping):
    pass

def time_roundtrip(id_to_time, trips=50, delay_between_trips = 0): #this is actually a bit incorrect because the timing of the "receive"
    #starts right after calling send which doesnt take into account the over the air send time (i think)
    send_times = []
    recieve_times = []
    for i in range(0, trips):
        start_time = int(time.perf_counter()*1000000)
        #ryrl.nonblockingrawsend()
        rylr.send(id_to_time, pack_octal(1,0,0,0,0))#ascii encoding here will be 2 bytes which is the same size as the octal commands
        #waitforresponce()                           #so it will take the same amount of time over uart as a hypothetical animation command
        for i in range(10000):
            if rylr.check_send_status():
                break
        recieve_start_time = int(time.perf_counter()*1000000)
        recieve_end_time = 0
        for i in range(10000):
            msg = rylr.receive()
            if not msg == None:
                    try:
                        decoded = msg.data.decode('ascii')
                        if decoded == 'rt':
                            recieve_end_time = int(time.perf_counter()*1000000)
                            break
                    except:
                        print('NA')
        
        end_time = int(time.perf_counter()*1000000)
        send_times.append(end_time-start_time)
        recieve_times.append(recieve_end_time-recieve_start_time)
        time.sleep(delay_between_trips)
        if delay_between_trips > 5:
            print(f'measurement of {end_time-start_time} taken')
    avg_send_time = sum(send_times) / len(send_times)
    avg_receive_time = sum(recieve_times) / len(recieve_times)
    print(f'''with {trips} roundtrip(s) measured to module #{id_to_time},
           average per roundtrip: {avg_send_time} microseconds, with average per send {avg_send_time-avg_receive_time} microseconds,
            and average per receive {avg_receive_time} microseconds''')


def ping_all():
    pass

#send to all nodes with delay for animations, to sent to all insantaniously send to id 0
def send_all(msg:str, delay_node=0, delay_branch=0):
    """ARGS > mesh:Mesh, module:RYLR998, delay_node:int(optional), delay_branch:int(optional)"""
    for branch in thismesh.mesh:
        for node in branch:
            print(f'sent to branch {branch}, node {node}, msg {msg}')
            rylr.send(node, msg.encode("ascii"))
            time.sleep(delay_node)
        time.sleep(delay_branch)
