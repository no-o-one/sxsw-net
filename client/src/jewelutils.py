import machine  # type:ignore
import neopixel #type:ignore
import time



jewel = neopixel.NeoPixel(machine.Pin(16, machine.Pin.OUT), 7) #7 is num of LEDs


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
