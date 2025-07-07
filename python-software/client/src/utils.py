import machine  # type:ignore
import neopixel #type:ignore
try:
    import src.reyax as reyax
except:
    import reyax
    print("!couldnt import reyax.py!")
    
import os
import random
import time

servo = machine.PWM(machine.Pin(17))
servo.freq(50)  # 50Hz for servo control
jewel = neopixel.NeoPixel(machine.Pin(16, machine.Pin.OUT), 7) #7 is num of leds
servo_last_angle = 180
current_animation = 'off' #track the current animation so that it can be broken out of


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



def jewel_set_all(r, g, b):
    for i in range(0, 7):
        jewel[i] = (r,g,b)
    jewel.write()


def jewel_set(list_of_tups): #takes a list of tuples of rg values for each led
    for i in range(0,7):
        jewel[i] = list_of_tups[i]
    jewel.write()



def file_system_setup():
    filestofind = ['reyax.py', 'utils.py', 'boot.py']
    for name in filestofind:
        if name not in os.listdir():
            print("!WARNING! "+name+" was not found in core directory")
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



def file_system_show():
    __traverse('', 1)



def __traverse(path, indent):
    for item in os.listdir(path):
        fullpath = path+'/'+item
        if not item.endswith('.py'):
            print('  '*indent + fullpath)
            __traverse(fullpath, indent+1)
        elif item.endswith('.py'):
            print('  '*indent + fullpath)



def servo_test():    
    for angle in range(0, 181, 30):
        servo_set_angle(angle)
        time.sleep(0.1)
    for angle in range(180, -1, -30):
        servo_set_angle(angle)
        time.sleep(0.1)
    print('motor test')



def servo_set_angle(angle):
    # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
    min_duty = 1638  # 1ms pulse (5% of 20ms)
    max_duty = 8192  # 2ms pulse (10% of 20ms)
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)


servo_set_angle(180)



def servo_rotate(to_angle):
    global servo_last_angle
    print('rotating form', servo_last_angle, 'to', to_angle)
    if to_angle > servo_last_angle:
        for deg in range(servo_last_angle, to_angle):
            servo_set_angle(deg)
            time.sleep(0.01)
    else:
        for deg in range(servo_last_angle, to_angle, -1):
            servo_set_angle(deg)
            time.sleep(0.01)
    servo_last_angle = to_angle
    print('rotated')



def connection_setup(self_address):
    try:
        uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))
        rylr = reyax.RYLR998(uart)
        rylr.address = self_address #9999 id reserved for host, 9998 for center; format of xxyy where xx branch no, yy node no
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


#ANIMATION RENDERERS--- will also have to actively check the current_animation because threading is a headache
def render_test_animation(speed=0.001):
    global current_animation
    for intensity in range(0, 256):
        if current_animation == 'test':
            jewel_set_all(intensity, 0, 0)
            time.sleep(speed)
        else:
            break
    for intensity in range(255, -1, -1):
        if current_animation == 'test':
            jewel_set_all(intensity, 0, 0)
            time.sleep(speed) 
        else: 
            break

    for intensity in range(0, 256):
        if current_animation == 'test':
            jewel_set_all(0, intensity, 0)
            time.sleep(speed)
        else:
            break
    for intensity in range(255, -1, -1):
        if current_animation == 'test':
            jewel_set_all(0, intensity, 0)
            time.sleep(speed)  
        else: 
            break

    for intensity in range(0, 256):
        if current_animation == 'test':
            jewel_set_all(0, 0, intensity)
            time.sleep(speed)
        else:
            break
    for intensity in range(255, -1, -1):
        if current_animation == 'test':
            jewel_set_all(0, 0, intensity)
            time.sleep(speed)  
        else:
            break
    current_animation = 'off'

def render_spotlight_animation():
    while current_animation == 'spotlight':
        jewel_set_all(50,50,50)

        if not current_animation == 'test':
            break
            
        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'test':
                break
        
        jewel_set_all(0,0,0)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'test':
                break
    
        jewel_set_all(100,100,100)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'test':
                break
        
        jewel_set_all(0,0,0)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'test':
                break

