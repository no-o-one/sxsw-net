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
    import src.jewelutils as jewelutils
except:
    print("!couldnt import jewelutils.py from src!")
try:
    import src.servoutils as servoutils
except:
    print("!couldnt import servoutils.py from src!")

import _thread
import uasyncio #type:ignore
import time
import os


print('> Setting up system')
lock = _thread.allocate_lock()    
host_id = 65535
self_id = 1 #placeholder
led_builtin = machine.Pin(25, machine.Pin.OUT)
utils.current_animation = 'none' #shared flag between all threads and utils.py
this_servo = servoutils.Servo()
this_jewel = jewelutils.Neopixel()
last_animation = 'none'
servo_timer = machine.Timer(-1)
nature_animation_sequence = []



def listen_to_host(): #this is the second core functionality
    while 1:
        received_msg = rylr.receive()
        if not received_msg == None:
            print(received_msg)
            data_parsed = received_msg.data.decode("ascii").split()
            #check received via imitating match-case; micropython does not have it :(

            #if not an animation command, handle command
            if data_parsed[0] == 'setallleds': #args > int:R, int:G, int:B
                utils.jewel_set_all(int(data_parsed[1]), int(data_parsed[2]), int(data_parsed[3]))

            elif data_parsed[0] == 'pyexec':
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
                utils.current_animation = 'off'
                lock.release()     
            
            elif data_parsed[0] == 'presettest':
                lock.acquire()
                utils.current_animation = 'test'
                lock.release()
            
            elif data_parsed[0] == 'presetspotlight':
                lock.acquire()
                utils.current_animation = 'spotlight'
                lock.release()     
            
            elif data_parsed[0] == 'presetnature':
                lock.acquire()
                utils.current_animation = 'nature'
                lock.release()
                
            elif data_parsed[0] == 'presetdystopia':
                lock.acquire()
                utils.current_animation = 'dystopia'
                lock.release()
                
            elif data_parsed[0] == 'presetirl':
                lock.acquire()
                utils.current_animation = 'irl'
                lock.release()
        time.sleep(0.2)


# async def animaiton_listener(lock): #async handles this loop in order to make it non blocking, and therefore permit acess to repl
#     try:
#         prev_anim = 'none' #avoiding double triggering - because the loop runs continiuously, there will be 
#         #a case that the animation name condition is triggered when the animation is already running, so it will interrupt the animation
#         #and start the same one again, which we are avoiding with this tracker
#         while 1:
#             lock.acquire()
#             cur_anim = utils.current_animation
#             lock.release()

#             if cur_anim == 'off' and prev_anim != cur_anim:
#                 utils.jewel_set_all(0, 0, 0)
#                 utils.servo_rotate(40)

#             elif cur_anim  == 'test' and prev_anim != cur_anim:
#                 utils.render_test_animation()

#             elif cur_anim  == 'spotlight' and prev_anim != cur_anim:
#                 utils.render_spotlight_animation()

#             elif cur_anim  == 'nature' and prev_anim != cur_anim:
#                 utils.render_nature_animation()

#             elif cur_anim  == 'irl' and prev_anim != cur_anim:
#                 utils.render_irl_animation(lock)

#             elif cur_anim  == 'dystopia' and prev_anim != cur_anim:
#                 utils.render_dystopia_animation()

#             await uasyncio.sleep(0.2)
#             prev_anim = cur_anim
#     except Exception as e:
#         print("!ASYNC EVENT LOOP CRASHED WITH THE FOLLOWING!", e)
#         await uasyncio.sleep(1)


print('> Setting up LoRa')
rylr = reyax.connection_setup(self_id)
print("> Setting up the file system")
utils.file_system_setup()

print('> Starting the second thread  for server')#only two per pico are possible
_thread.start_new_thread(listen_to_host, ())#empty tuple is args


bounce_servo = utils.AnimationInstance(id = 1, curve = 'bounce', seconds = 2, fps = 100, end_keyframe = 180)
callcount = 0
def bounce_servo_callback(timer):
    global callcount
    global last_animation
    if callcount <= bounce_servo.total_frames:
        this_servo.set_angle(int(bounce_servo.compute(callcount)))
        callcount += 1
    else: 
        last_animation = 'none'
        callcount = 0
        timer.deinit()

#TODO: REPL GRACE PERIOD HERE

while True: #i will regret this 
    lock.acquire()
    cur_anim_local = utils.current_animation
    lock.release()
    
    if last_animation != cur_anim_local:
        if cur_anim_local == 'nature':
            servo_timer.init(mode = machine.Timer.PERIODIC, period = bounce_servo.ms_between_frames, callback = bounce_servo_callback)
        elif cur_anim_local == 'off':
            this_servo.set_angle(0)
            servo_timer.deinit()
    
    last_animation = cur_anim_local
    time.sleep_ms(1)



