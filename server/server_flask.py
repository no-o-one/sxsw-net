import serial
import serial.tools.list_ports
import code

from src.reyax import *
from src.utils import *
import src.pyserialwrapper as pyserialwrapper
import time

from flask import Flask, jsonify, request
from threading import Thread
import time

app = Flask(__name__)



def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2],16) for i in (0, 2, 4))


def send_params(json):
    print("REQUEST!")
    #preprocess
    type_nkwrd = json["type"]
    from_nkwrd = json["from"]
    to = json["to"]
    time_nkwrd = json["time"]
    curve = json["curve"]
    #conversions
    #convert float to 10-170 val and hex to rgb sequence
    if type(from_nkwrd) == float and type(to) == float:
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

    cmd = f"cmd {type_nkwrd} {from_nkwrd} {to} {time_nkwrd} {curve}"
    rylr.send(1, cmd.encode('ascii'))




# === Flask routes that trigger your functions ===
from flask import request, jsonify
from threading import Thread

@app.route('/', methods=['POST'])
def run_loop_example():
    print("hi")

    content_type = request.headers.get('Content-Type')
    print("Content-Type:", content_type)

    if content_type and 'application/json' in content_type:
        print("getting json")
        data = request.get_json(silent=True)
        print("received:", data)

        Thread(target=send_params, args=(data,)).start()

        return jsonify({"status": "ok"})  # ✅ REQUIRED
    else:
        print("content type not json")
        return jsonify({"error": "Expected application/json"}), 400


# === Function to start Flask server ===
def run_flask_app():
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=1234)

# === Start Flask in background thread ===
flask_thread = Thread(target=run_flask_app, daemon=True)
flask_thread.start()


#prompt for portname to connect
port = "COM5" #USB PORT


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

