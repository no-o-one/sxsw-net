import serial
import serial.tools.list_ports
import code

import src.reyax as reyax
import src.pyserialwrapper as pyserialwrapper
import time

from flask import Flask, jsonify
from threading import Thread
import time

app = Flask(__name__)



def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2],16) for i in (0, 2, 4))


def send_params(json):
    #preprocess
    type_nkwrd = json["from"]
    from_nkwrd = json["from"]
    to = json["to"]
    time_nkwrd = json["time"]
    curve = json["curve"]
    #conversions
    #convert float to 10-170 val and hex to rgb sequence
    if type(from_nkwrd == float) and type(to == float):
        from_nkwrd = (from_nkwrd*160)+10
        from_nkwrd = str(int(from_nkwrd))

        to = (to*160)+10
        to = str(int(to))
    elif type(from_nkwrd == str) and type(to == str):
        from_nkwrd = hex_to_rgb(from_nkwrd)
        from_nkwrd = (f"{str(from_nkwrd[0])} {str(from_nkwrd[1])} {str(from_nkwrd[2])}")
    
        to = hex_to_rgb(to)
        to = (f"{str(to[0])} {str(to[1])} {str(to[2])}")
    
    time_nkwrd = str((time_nkwrd/1000))

    if type_nkwrd == "color":
        type_nkwrd = "this_jewel"
    elif type_nkwrd == "position":
        type_nkwrd = "this_servo"

    cmd = f"cmd {type_nkwrd} {from_nkwrd} {to} {time_nkwrd} {curve}"
    rylr.send(1, cmd.enconde('ascii'))



def bandf():
    for i in range(1, 100):
        rylr.send(1, b"pyexec this_servo.set(15)") 
        rylr.send(1, b"pyexec this_servo.set(165)")
        time.sleep(10)

def demo_talk():
    rylr.send(1, b"pyexec j_transit.play()")
    time.sleep(2)
    rylr.send(1, b"pyexec s_open_more.play()")
    time.sleep(0.5)
    rylr.send(1, b"pyexec j_open_more.play()")
    print("sent 1")
    time.sleep(3.5)
    rylr.send(1, b"pyexec soft_open_late_loop.play()")
    print("sent 2")
    # rylr.send(1, b"pyexec soft_open_late.play()")
    # print("sent 3")
    # time.sleep(7)
    # rylr.send(1, b"pyexec j_bloom_pink.play()")
    # print("sent 4")
    # time.sleep(0.5)
    # rylr.send(1, b"pyexec soft_open_late_loop.play()")
    # print("sent 5")

def demo_talk_kill():
    rylr.send(1, b"pyexec j_open_more.kill()")
    print("sent 4")
    time.sleep(0.5)
    rylr.send(1, b"pyexec soft_open_late_loop.kill()")
    print("sent 4")
    time.sleep(0.5)
    rylr.send(1, b"pyexec j_bloom_warmup_die.play()")
    time.sleep(1)
    rylr.send(1, b"pyexec this_servo.set(0)")
    # rylr.send(1, b"pyexec s_warmup_close.play()")
    # time.sleep(0.5)
    # rylr.send(1, b"pyexec this_servo.set(100)")
    # time.sleep(0.5)
    # rylr.send(1, b"pyexec this_jewel.set(0)")

def warmup():
    rylr.send(1, b"pyexec this_jewel.set(0)")
    time.sleep(0.5)
    rylr.send(1, b"pyexec this_servo.set(0)")
    time.sleep(2)
    rylr.send(1, b"pyexec j_bloom_warmup.play()")
    time.sleep(2)
    rylr.send(1, b"pyexec s_warmup_open.play()")

def warmup_close():
    pass

def warmup_close_key1():
    rylr.send(1, b"pyexec this_jewel.set([75, 9, 1])")
    time.sleep(0.5)
    rylr.send(1, b"pyexec this_servo.set(100)")

def reset():
    rylr.send(1, b"pyexec this_jewel.set(0)")
    time.sleep(0.5)
    rylr.send(1, b"pyexec this_servo.set(0)")


# === Flask routes that trigger your functions ===
@app.route('/', methods=['POST'])
def run_loop_example():
    #check if json
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json#dict type
        #send params in a separate thread
        Thread(target=send_params, args=(json)).start()  # Run asynchronously
    else:
        print("content type not json")
    




#first list al of the ports available on the device and compare prior to/after plugging hte module in
print("> current port list \n")
ports = serial.tools.list_ports.comports()
available_ports = []
for port in ports:
    print(f"Port: {port.device} | Description: {port.description}")
    available_ports.append(port.device)
print("\n")

input("> press enter when plugged in the module \n")

print("> new port list \n")
ports = serial.tools.list_ports.comports()
available_ports = []
for port in ports:
    print(f"Port: {port.device} | Description: {port.description}")
    available_ports.append(port.device)
print("\n")

#prompt for portname to connect
port = input("> enter the port name the rylr should be on \n")


#connect to module
baudrate = 115200
try:
    uart = pyserialwrapper.pyserialUARTwrapper(port, baudrate)
    rylr = reyax.RYLR998(uart)
    rylr.address = 65535
    if not rylr.pulse:
        print('!WARNING! LoRa module test failed')
    else:
        print("connected")
except Exception as e:
    print(f'!WARNING! Connection to LoRa at {port} with baudrate {baudrate} failed with the following: \n{e}')

# Start interactive shell (REPL) in main thread
print("> Setup finished, opening REPL for debug...")#exit() or ctrl+D to exit repl, the daemon thread will be killed automatically
code.interact(local=locals())

print("> REPL exited, killing all threads...")





# === Function to start Flask server ===
def run_flask_app():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)

# === Start Flask in background thread ===
flask_thread = Thread(target=run_flask_app, daemon=True)
flask_thread.start()

