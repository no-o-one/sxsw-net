from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import src.pyserialwrapper as pyserialwrapper
import src.reyax as reyax
from src.Mesh import *
import src.utils as utils
import time
import random
import code



#LORA MODULE SETUP
port = '/dev/tty.placeholder'
baudrate = 115200
try:
    uart = pyserialwrapper.pyserialUARTwrapper(port, baudrate)
    rylr = reyax.RYLR998(uart)
    if not rylr.pulse:
        print('!WARNING! LoRa module test failed')
except Exception as e:
    print(f'!WARNING! Connection to LoRa at {port} with baudrate {baudrate} failed with the following: \n{e}')
#--
#setup existing mesh of nodes
thismesh = Mesh([[0, 1]])


def print_osc(address, *args):
    print("Received "+ address +" with args:")
    for argument in args:
        print(f"{argument}:{type(argument).__name__}")
    print("\n")



#MESSAGE HANDLERS
#adress passes the OSC command that triggered the handler, *args is then an undefined sized tuple
def preset_handler(address, *args): #should get str:preser_name
    match args[0]:
        case 'off':
            print('GOT: OFF')
            utils.send_all_nodes(thismesh, rylr, 'presetoff')

        case 'test':
            print('GOT: TEST')
            utils.send_all_nodes(thismesh, ryflr, 'presettest')
            
        case 'spotlight':
            print("GOT: SPOTLIGHT")
            utils.send_all_nodes(thismesh, rylr, 'presetspotlight')

        case 'nature':
            print('GOT: NATURE')
            utils.send_all_nodes(thismesh, rylr, 'setallleds 116 163 66')

        case 'dystopia':
            pass
        case 'irl':
            pass

def fadein_handler(address, *args): #should get str:preset_name, int:fade_ms
    print_osc(address, *args)

def transition_handler(address, *args): #should get str:preset_name, int:fade_ms
    print_osc(address, *args)

def transient_handler(address, *args): #should get int:duration_ms, ?:intensity, str:next_prest
    print_osc(address, *args)


ip ="127.0.0.1" #localhost
port = 8080 #qlab listens to this port for feedback by defualt

dispatcher = Dispatcher() #create disptcher for message routing 
dispatcher.map("/flowerlights/preset", preset_handler) #map the OSC commands to handler functions 
dispatcher.map("/flowerlights/fadein", fadein_handler)
dispatcher.map("/flowerlights/transition", transition_handler)
dispatcher.map("/flowerlights/transient", transient_handler)

server = BlockingOSCUDPServer((ip, port), dispatcher) #blocking server as in in blocks the main thread until program is aborted

print("! SERVER STARTED ON " + ip + ":" + str(port) + "! Listening in progress...")
server.serve_forever() # !!!blocks the main thread

#TODO: implement starting server on adifferent threading to enable repl acess later to pin gte nodes for example and other debug
#print("> Setup finished, opening REPL for debug...")
# Start interactive shell
#code.interact(local=locals())