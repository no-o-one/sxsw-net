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
import time
import os
from sys import print_exception


print('> Setting up system')
lock = _thread.allocate_lock()    
host_id = 65535
self_id = 1 #placeholder
led_builtin = machine.Pin(25, machine.Pin.OUT)

animationutils.current_animation_flag = 'none' #shared flags between all threads and utils.py
animationutils.last_animation_flag = 'none'





def listen_to_host(): #this is the second core functionality
    while 1:
        received_msg = rylr.receive()
        if not received_msg == None:
            print(received_msg)
            data_parsed = received_msg.data.decode("ascii").split()
            #check received via imitating match-case; micropython does not have it :(

            #if not an animation command, handle command
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

            #if an anitmaiton command, change the current_animation flag
            elif data_parsed[0] == 'presetoff':
                lock.acquire()
                animationutils.current_animation_flag = 'off'
                lock.release()     
            
            elif data_parsed[0] == 'presettest':
                lock.acquire()
                animationutils.current_animation_flag = 'test'
                lock.release()
            
            elif data_parsed[0] == 'presetspotlight':
                lock.acquire()
                animationutils.current_animation_flag = 'spotlight'
                lock.release()     
            
            elif data_parsed[0] == 'presetnature':
                lock.acquire()
                animationutils.current_animation_flag = 'nature'
                lock.release()
                
            elif data_parsed[0] == 'presetdystopia':
                lock.acquire()
                animationutils.current_animation_flag = 'dystopia'   
                lock.release()
                
            elif data_parsed[0] == 'presetirl':
                lock.acquire()
                animationutils.current_animation_flag = 'irl' 
                lock.release()
        time.sleep_ms(1)


print('> Setting up LoRa')
rylr = reyax.connection_setup(self_id)
print("> Setting up the file system")
utils.file_system_setup()

print('> Starting the second thread  for server....')#only two per pico are possible
_thread.start_new_thread(listen_to_host, ())#empty tuple is args

#TODO: REPL GRACE PERIOD HERE  
while True: #start actively tracking animations
    try:
        lock.acquire() 
        cur_anim_local = animationutils.current_animation_flag  
        lock.release() 
        if animationutils.last_animation_flag != cur_anim_local:   
            if animationutils.last_animation_flag != 'none':
                animationutils.AnimationInstance.kill_all() 
            if cur_anim_local == 'nature':
                nature_animation.reset()
                nature_animation.play() 
            elif cur_anim_local == 'off':
                this_servo.set(0)
                this_jewel.set(0)
            elif cur_anim_local == 'irl':
                irl_animation.reset()
                irl_animation.play()
            elif cur_anim_local == 'dystopia':
                irl_animation.reset()
                irl_animation.play()
                nature_animation.reset()
                nature_animation.play() 
    
        animationutils.last_animation_flag = cur_anim_local  
        time.sleep_ms(1)
    except Exception as e:
        print_exception(e)
        break





