import machine  # type:ignore
import neopixel #type:ignore
import src.reyax
import os
import time

servo = machine.PWM(machine.Pin(17))
servo.freq(50)  # 50Hz for servo control
jewel = neopixel.NeoPixel(machine.Pin(16, machine.Pin.OUT), 7) #7 is num of leds

def jewel_test():
    jewel[0] = (0, 255, 0)
    jewel[1] = (255, 0, 0)
    jewel[2] = (0, 0, 255)
    jewel[3] = (255, 255, 255)
    jewel[4] = (120, 120, 0)
    jewel[5] = (0, 120, 120)
    jewel[6] = (120, 0, 120)
    jewel.write()
    
    time.sleep(5)

    jewel[0] = (0,0,0)
    jewel[1] = (0,0,0)
    jewel[2] = (0,0,0)
    jewel[3] = (0,0,0)
    jewel[4] = (0,0,0)
    jewel[5] = (0,0,0)
    jewel[6] = (0,0,0)
    jewel.write()
    print('jewel test done')

def setup_file_system():
    filestofind = ['reyax.py', 'utils.py', 'boot.py']
    for name in filestofind:
        if name not in os.listdir():
            print("!WARNING! "+name+" was not found.")
    if 'src' not in os.listdir():
        os.mkdir('src')
    try: 
        os.rename('reyax.py', 'src/reyax.py')
    except:
        print('!WARNING! reyax.py has not been relocated')
    try:
        os.rename('utils.py', 'src/utils.py')
    except:
        print('!WARNING! utils.py has not been relocated')

def show_file_system():
    traverse('', 1)


def traverse(path, indent):
    for item in os.listdir(path):
        fullpath = path+'/'+item
        if not item.endswith('.py'):
            print('  '*indent + fullpath)
            traverse(fullpath, indent+1)
        elif item.endswith('.py'):
            print('  '*indent + fullpath)


def servo_test():    
    for angle in range(0, 181, 30):
        set_angle(angle, servo)
        time.sleep(0.1)
    for angle in range(180, -1, -30):
        set_angle(angle, servo)
        time.sleep(0.1)
    print('motor test')

def set_angle(angle, servo):
    # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
    min_duty = 1638  # 1ms pulse (5% of 20ms)
    max_duty = 8192  # 2ms pulse (10% of 20ms)
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

def setup_connection(self_address):
    try:
        uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))
        rylr = src.reyax.RYLR998(uart)
        rylr.address = self_address #9999 id reserved for central unit; format of xxyy where xx branch no, yy node no
        if not rylr.pulse:
            print('!WARNING! LoRa module test failed')
    except Exception as e:
        print("!WARNING! Failed to set up the LoRa module with the following exception:")
        print(e)
        pass

    print('Connected network id: ', rylr.networkid) #18 by default, i will leave it like that
    print('Connected module address: ', rylr.address)
    msg = "Module address #" + str(rylr.address) + " has connected to the network."
    rylr.send(9999, msg.encode("ascii"))
    return rylr


