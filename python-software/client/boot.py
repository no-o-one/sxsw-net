try:
    import src.reyax as reyax
except:
    print("!couldnt import reyax.py!")
import os
import time
import neopixel
try:
    import src.utils as utils
except:
    print("!couldnt import utils.py!")
    import utils
import _thread


lock = _thread.allocate_lock()    
host_id = 9999
self_id = 2 #0001
led_builtin = machine.Pin(25, machine.Pin.OUT)
utils.current_animation = 'off'


def test_all():
    rylr.send(host_id, "testing motors!".encode("ascii"))
    print("testing motors!")
    utils.servo_test()
    rylr.send(host_id, "testing jewel!".encode("ascii"))
    print("testing jewel!")
    utils.jewel_test()
    rylr.send(host_id, "done!".encode("ascii"))
    print("done!")
    rylr.send(host_id, "setting servo to 0".encode("ascii"))
    print("setting servo to 0")
    utils.servo_set_angle(0)   



def listen_to_host(): #also tracks current
    while 1:
        received_msg = rylr.receive()
        if not received_msg == None:
            print(received_msg)
            data_parsed = received_msg.data.decode("ascii").split()
            #check if addressed to self
            if data_parsed[0] == str(self_id) or data_parsed[0] == 'all':
                #check received via imitating match-case for micropython does not have it :(
                if data_parsed[1] == 'setallleds': #args > int:R, int:G, int:B
                    utils.jewel_set_all(int(data_parsed[1]), int(data_parsed[2]), int(data_parsed[3]))

                elif data_parsed[1] == 'presetoff':
                    print('got off')
                    lock.acquire()
                    utils.current_animation = 'off'
                    lock.release()
                    utils.jewel_set_all(0,0,0)
                    utils.servo_rotate(40)
                    utils.jewel_set_all(0,0,0)
                    utils.jewel_set_all(0,0,0)
                

                elif data_parsed[1] == 'presettest':
                    print('got test')
                    lock.acquire()
                    utils.current_animation = 'test'
                    lock.release()
                
                elif data_parsed[1] == 'presetspotlight':
                    print('got spotlight')
                    lock.acquire()
                    utils.current_animation = 'spotlight'
                    lock.release()
                    utils.servo_rotate(40)
                    utils.jewel_set_all(0, 0, 0)
                    utils.jewel_set_all(90,90,90)
                    utils.servo_rotate(180)
                
                elif data_parsed[1] == 'presetnature':
                    print('got spotlight')
                    lock.acquire()
                    utils.current_animation = 'nature'
                    lock.release()
                    print('got nature')
                    utils.servo_rotate(40)
                    utils.jewel_set_all(0, 0, 0)
                    utils.jewel_set_all(180,250,40)
                    utils.servo_rotate(180)
                
                elif data_parsed[1] == 'presetdystopia':
                    print('got spotlight')
                    lock.acquire()
                    utils.current_animation = 'dystopia'
                    lock.release()
                    utils.servo_rotate(40, 0.005)
                    utils.jewel_set_all(0, 0, 0)
                    utils.jewel_set_all(250,0,0)
                    

                elif data_parsed[1] == 'presetirl':
                    print('got spotlight')
                    lock.acquire()
                    utils.current_animation = 'irl'
                    lock.release()
                    utils.servo_rotate(40)
                    utils.jewel_set_all(0, 0, 0)
                    utils.jewel_set_all(180,10,190)
                    utils.servo_rotate(180)
                    
                
        time.sleep(0.1)


def listen_to_anim_state():
    lock.acquire()
    current_anim = utils.current_animation 
    lock.release()

    if current_anim == 'off':
        utils.jewel_set_all(0, 0, 0)
        utils.servo_rotate(40)

    elif current_anim == 'test':
        utils.render_test_animation()

    elif current_anim == 'spotlight':
       utils.render_test_animation()

    elif current_anim == 'nature':
       utils.render_nature_animation()

    elif current_anim == 'irl':
       utils.render_irl_animation()

    elif current_anim == 'dystopia':
       utils.render_dystopia_animation()

    time.sleep(0.1)




print('> Setting up LoRa')
rylr = utils.connection_setup(self_id)

print("> Setting up the file system")
utils.file_system_setup()

print('> Starting the server thread')#only two per pico are possible
_thread.start_new_thread(listen_to_host, ())#empty tuple is args

# print('> Starting the animation tracking thread')
# for i in range(0, 500): 
#     listen_to_anim_state()
#     time.sleep(0.1)
    


