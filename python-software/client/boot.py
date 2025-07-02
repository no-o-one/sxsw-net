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



def listen_to_host():
    while 1:
        received_msg = rylr.receive()
        if not received_msg == None:
            data_parsed = received_msg.data.decode("ascii").split()
            #check if addressed to self
            if data_parsed[0] == 'all' or int(data_parsed) == self_id:
                #check received
                match data_parsed[1]:
                    case 'setallleds': #setallleds int:R int:G int:B
                        utils.jewel_set_all(data_parsed[2], data_parsed[3], data_parsed[4])
                    case 'placeholder':
                        pass
                    
    time.sleep(0.1)



print('\n> Setting up LoRa\n')
rylr = utils.connection_setup(self_id)

print("\n> Setting up the file system\n")
utils.file_system_setup()

print('\n> Starting the second thread\n')#only two per pico are possible
_thread.start_new_thread(listen_to_host, ())#empty tuple is args

