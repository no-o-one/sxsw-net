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
import uasyncio

servo = machine.PWM(machine.Pin(17))
servo.freq(50)  # 50Hz for servo control
jewel = neopixel.NeoPixel(machine.Pin(16, machine.Pin.OUT), 7) #7 is num of LEDs
servo_last_angle = 180
current_animation = 'none' #shared flag between two cores and boot.py


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
    print('> Jewel test done')



def jewel_set_all(r, g, b):
    """ARGS > r:int (0-255), g:int (0-255), b:int (0-255)"""
    global jewel
    for i in range(0, 7):
        jewel[i] = (r,g,b)
        jewel.write()
    


def jewel_set(list_of_tups):
    """ARGS > list_of_tups:list (each tuple contains r:int (0-255), g:int (0-255), b:int (0-255)
    for the corresponding led on the jewel; list must be 7 items long because og this)"""
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


#TODO: precentage impl. use 40 as a placeholder for now
def servo_set_angle(angle):
    # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
    min_duty = 1638  # 1ms pulse (5% of 20ms)
    max_duty = 8192  # 2ms pulse (10% of 20ms)
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)


#TODO: precentage impl. use 40 as a placeholder for now
def servo_rotate(to_angle, speed = 0.01):
    """ARGS > to_angle:int, speed:int (optional wait time inbetween steps in seconds; 0.01 by default)"""
    global servo_last_angle
    print('> Rotating form', servo_last_angle, 'to', to_angle)
    if to_angle > servo_last_angle:
        for deg in range(servo_last_angle, to_angle):
            servo_set_angle(deg)
            time.sleep(speed)
    else:
        for deg in range(servo_last_angle, to_angle, -1):
            servo_set_angle(deg)
            time.sleep(speed)
    servo_last_angle = to_angle
    print('rotated')



def connection_setup(self_address):
    """ARGS > self_adress:int (address can be 0 - 65535)"""
    try:
        uart = machine.UART(1, baudrate=115200, tx=machine.Pin(4), rx=machine.Pin(5))
        rylr = reyax.RYLR998(uart)
        rylr.address = self_address
        if not rylr.pulse:
            print('!WARNING! LoRa module test failed')
    except Exception as e:
        print("!WARNING! Failed to set up the LoRa module with the following exception:")
        print(e)
        pass

    print('> Connected network id: ', rylr.networkid) #18 by default, i will leave it like that
    print('> Connected module address: ', rylr.address)
    msg = "> Module address #" + str(rylr.address) + " has connected to the network."
    rylr.send(9999, msg.encode("ascii"))
    return rylr


#ANIMATION RENDERERS--- will also have to actively check the current_animation because threading is a  - this is terrifying please whta the fuck
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
    global current_animation
    while current_animation == 'spotlight':
        jewel_set_all(50,50,50)
        servo_rotate(80, 0.005)

        if not current_animation == 'spotlight':
            break
            
        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'spotlight':
                break
        
        jewel_set_all(0,0,0)
        servo_rotate(140, 0.005)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'spotlight':
                break
    
        jewel_set_all(100,100,100)
        servo_rotate(80, 0.005)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'spotlight':
                break
        
        jewel_set_all(0,0,0)
        servo_rotate(140, 0.005)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'spotlight':
                break



def render_dystopia_animation():
    global current_animation
    while current_animation == 'dystopia':
        jewel_set_all(50,50,50)
        servo_rotate(80, 0.005)

        if not current_animation == 'dystopia':
            break
            
        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'dystopia':
                break
        
        jewel_set_all(150,0,0)
        servo_rotate(140, 0.005)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'dystopia':
                break
    
        jewel_set_all(100,100,100)
        servo_rotate(80, 0.005)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'dystopia':
                break
        
        jewel_set_all(100,0,0)
        servo_rotate(140, 0.005)

        to = time.sleep(random.randint(1, 10))
        for wait in range(0, to, 0.2):
            time.sleep(wait)
            if not current_animation == 'dystopia':
                break


def render_nature_animation():
    global current_animation
    jewel_set_all(111,158,93)
    if not current_animation == 'nature':
        pass
    servo_rotate(180, 0.02)
    if not current_animation == 'nature':
        pass

    jewel_set_all(111,148,113)
    if not current_animation == 'nature':
        pass
    servo_rotate(140, 0.02)
    if not current_animation == 'nature':
        pass



async def render_irl_animation(lock):#uasyncio.sleep(0) are sprinkled in here to make sure other functions in boot.py still run
    global current_animation
    
    #light up softly white
    for i in range(0, 10):
        jewel_set_all(i, i, i)
        await uasyncio.sleep(0.05)

    #open
    servo_rotate(40)
    await uasyncio.sleep(0)
    servo_rotate(70, 0.008)
    await uasyncio.sleep(0)
    servo_rotate(110, 0.012)
    await uasyncio.sleep(0)
    servo_rotate(160, 0.018)
    await uasyncio.sleep(0)
    servo_rotate(180, 0.026)
    await uasyncio.sleep(0)

    #fade to purple 90, 10, 130
    for i in range(10, 130):
        if i < 90:
            jewel_set_all(i, 10, i)
        else:
           jewel_set_all(90, 10, i) 
        await uasyncio.sleep(0.05)
    
    #chill
    await uasyncio.sleep(5)

    #close
    servo_rotate(160, 0.026)
    await uasyncio.sleep(0)
    servo_rotate(110, 0.018)
    await uasyncio.sleep(0)
    servo_rotate(70, 0.012)
    await uasyncio.sleep(0)
    servo_rotate(40, 0.008)
    await uasyncio.sleep(0)
   
    #reset animation done, reset the tracker in a safe fashion so that the animation can re trigger if needed
    lock.acquire()
    current_animation = 'none'
    lock.release()
