from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import src.utils as utils
import code
import threading



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
            msg = [0,0,0,0,0]
            utils.rylr.send(1, utils.pack_octal(*msg))

        case 'test':
            print('GOT: TEST')
            msg = [0,0,0,0,1]
            utils.rylr.send(1, utils.pack_octal(*msg))
            
        case 'spotlight':
            print("GOT: SPOTLIGHT")
            msg = [0,0,0,0,2]
            utils.rylr.send(1, utils.pack_octal(*msg))

        case 'nature':
            print('GOT: NATURE')
            msg = [0,0,0,0,3]
            utils.rylr.send(1, utils.pack_octal(*msg))

        case 'dystopia':
            print('GOT: DYST')
            msg = [0,0,0,0,4]
            utils.rylr.send(1, utils.pack_octal(*msg))

        case 'irl':
            print('GOT: IRL')
            msg = [0,0,0,0,5]
            utils.rylr.send(1, utils.pack_octal(*msg))
                   

def fadein_handler(address, *args): #should get str:preset_name, int:fade_ms
    print_osc(address, *args)

def transition_handler(address, *args): #should get str:preset_name, int:fade_ms
    print_osc(address, *args)

def transient_handler(address, *args): #should get int:duration_ms, ?:intensity, str:next_prest
    print_osc(address, *args)


ip ="127.0.0.1" #localhost
port = 8080

dispatcher = Dispatcher() #create disptcher for message routing 
dispatcher.map("/flowerlights/preset", preset_handler) #map the OSC commands to handler functions 
dispatcher.map("/flowerlights/fadein", fadein_handler)
dispatcher.map("/flowerlights/transition", transition_handler)
dispatcher.map("/flowerlights/transient", transient_handler)

server = BlockingOSCUDPServer((ip, port), dispatcher) #blocking server as in in blocks the main thread until program is aborted


def start_server():
    print("> !SERVER STARTED ON " + ip + ":" + str(port) + "! Listening in the background...")
    server.serve_forever()

# Start the server in a daemon thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Start interactive shell (REPL) in main thread
print("> Setup finished, opening REPL for debug...")#exit() or ctrl+D to exit repl, the daemon thread will be killed automatically
code.interact(local=locals())

print("> REPL exited, killing all threads...")

