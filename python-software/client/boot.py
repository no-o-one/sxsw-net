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

    
host_id = 9999
self_id = 1 #0001
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
            data_parsed = received_msg.data.decode("ascii").split()
            #check if addressed to self
            if received_msg.address == self_id:
                #check received via imitating match-case for micropython does not have it :(
                if data_parsed[0] == 'setallleds': #args > int:R, int:G, int:B
                    utils.jewel_set_all(int(data_parsed[1]), int(data_parsed[2]), int(data_parsed[3]))

                elif data_parsed[0] == 'presetoff':
                    utils.current_animation = 'off'
                    utils.jewel_set_all(0, 0, 0)

                elif data_parsed[0] == 'presettest':
                    utils.current_animation = 'test'
                    utils.render_test_animation()
                
                elif data_parsed[0] == 'presetspotlight':
                    utils.current_animation = 'spotlight'
                    utils.render_spotlight_animation()

        time.sleep(0.1)



print('> Setting up LoRa')
rylr = utils.connection_setup(self_id)

print("> Setting up the file system")
utils.file_system_setup()

print('> Starting the second thread')#only two per pico are possible
_thread.start_new_thread(listen_to_host, ())#empty tuple is args


