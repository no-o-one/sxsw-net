import src.reyax as reyax
import os
import time
import neopixel
import src.utils as utils

host_id = 9999
self_id = 0000

led = machine.Pin(25, machine.Pin.OUT)

led.toggle()     
time.sleep(5)
led.toggle()     


rylr = utils.setup_connection(self_id)

rylr.send(host_id, "testing motors!".encode("ascii"))
utils.servo_test()
rylr.send(host_id, "testing jewel!".encode("ascii"))
utils.jewel_test()
rylr.send(host_id, "done!".encode("ascii"))

