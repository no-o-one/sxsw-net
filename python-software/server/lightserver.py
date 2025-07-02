import pythonosc
import src.wrapper as wrapper
import src.reyax as reyax



#LORA MODULE SETUP
port = '/dev/tty.placeholder'
baudrate = 115200
try:
    uart = wrapper.pyserialUARTwrapper(port, baudrate)
    rylr = reyax.RYLR998(uart)
    if not rylr.pulse:
        print('!WARNING! LoRa module test failed')
except Exception as e:
    print(f'!WARNING! Connection to LoRa at {port} with baudrate {baudrate} failed with the following: \n\n{e}')
#--



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
            pass
        case 'test':
            rylr.send(f'all setallleds {str(args[1])} {str(args[2])} {str(args[3])}')
        case 'spotlight':
            pass
        case 'nature':
            pass
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
port = 53000 #qlab listens to this port for feedback by defualt

dispatcher = pythonosc.dispatcher.Dispatcher() #create disptcher for message routing 
dispatcher.map("/flowerlights/preset", preset_handler) #map the OSC commands to handler functions 
dispatcher.map("/flowerlights/fadein", fadein_handler)
dispatcher.map("/flowerlights/transition", transition_handler)
dispatcher.map("/flowerlights/transient", transient_handler)

server = pythonosc.osc_server.BlockingOSCUDPServer((ip, port), dispatcher) #blocking server as in in blocks the main thread until program is aborted

print("! SERVER STARTED ON " + ip + ":" + str(port) + "! Listening in progress...")
server.serve_forever() # !!!blocks the main thread
