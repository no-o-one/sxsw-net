import time

import machine #type:ignore
try:
    import src.reyax as reyax
except:
    print("!couldnt import reyax.py from src!")
try:
    import src.utils as utils
except:
    print("!couldnt import utils.py from src!")
    import utils #type:ignore
try:
    from src.animations import *
except:
    print("!couldnt import animations.py from src!")

import _thread	
import os
from sys import print_exception


led = machine.Pin(25, machine.Pin.OUT)

print('> Setting up system')
lock = _thread.allocate_lock()    
host_id = 65535
self_id = 1 #placeholder
led_builtin = machine.Pin(25, machine.Pin.OUT)

animationutils.current_animation_flag = 'none' #shared flags between all threads and utils.py
animationutils.last_animation_flag = 'none'

reference = {
    0:'off',
    1:'test',
    2:'spotlight',
    3:'nature',
    4:'dystopia',
    5:'irl'
}

def listen_to_host(): #this is the second core functionality
    while 1:
        received_msg = rylr.receive()
        if not received_msg == None:
            #print(received_msg)

            #if not 2 bytes, so is not an octal command, handle command
            if len(received_msg.data) !=2:
                data_parsed = received_msg.data.decode("ascii").split()
                if data_parsed[0] == 'pyexec':
                    command = received_msg.data.decode("ascii")[7:]
                    try:
                        exec(command)
                    except Exception as e:
                        print(e)

                elif data_parsed[0] == 'nuke':#failsafe/remote debugging - deletes boot py in case it blocks serial/fails something else
                    print('got nuke, dleteing boot and restetting machine...')
                    os.remove('boot.py')
                    machine.reset()

            else:
                #if an octal command, change the current_animation flag/process
                msg_unpacked = utils.unpack_octal(received_msg.data) 
                if msg_unpacked[0]==1:
                    rylr.send(host_id, 'rt'.encode('ascii'))
                else:
                    lock.acquire()
                    animationutils.current_animation_flag = reference[msg_unpacked[-1]]
                    lock.release()
                    #print(msg_unpacked[-1])
                

        time.sleep_us(10)

led.on() 
print('> Setting up LoRa')
rylr = reyax.safe_reyax_connection_setup(self_id)
led.off()
print("> Setting up the file system")
utils.file_system_setup()


print('> Starting the second thread  for server....')#only two per pico are possible
_thread.start_new_thread(listen_to_host, ())#empty tuple is args
#TODO: REPL GRACE PERIOD HERE

print("workin")
while True: #start actively tracking animations
    try:
        lock.acquire() 
        cur_anim_local = animationutils.current_animation_flag  
        lock.release() 
        if animationutils.last_animation_flag != cur_anim_local:   
            if animationutils.last_animation_flag != 'none':
                animationutils.AnimationInstance.kill_all() 
            if cur_anim_local == 'test':
                servo_test.reset(); jewel_test.reset()
                servo_test.play(); jewel_test.play()

            elif cur_anim_local == 'spotlight':
                servo_spotlight.reset(); jewel_spotlight.reset()
                servo_spotlight.play(); jewel_spotlight.play()

            elif cur_anim_local == 'nature':
                servo_nature.reset(); jewel_nature.reset()
                servo_nature.play(); jewel_nature.play()

            elif cur_anim_local == 'dystopia':
                servo_dystopia.reset(); jewel_dystopia.reset()
                servo_dystopia.play(); jewel_dystopia.play()

            elif cur_anim_local == 'irl':
                servo_irl.reset(); jewel_irl.reset()
                servo_irl.play(); jewel_irl.play()

            elif cur_anim_local == 'off':
                this_servo.set(0) 
                this_jewel.set(0)
    
        animationutils.last_animation_flag = cur_anim_local  
        time.sleep_us(10)
    except Exception as e:
        print_exception(e)
        break