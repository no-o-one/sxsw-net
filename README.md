# Hardware documentation 

[pcb files!](https://drive.google.com/drive/folders/1o0MN87YVfZmZX_xxKThMRZH78RT8oLCC?usp=drive_link)

**parts client side**
- Non W Raspberry Pi pico with RP2040 flashed with [Micropython v1.125.0](https://micropython.org/download/RPI_PICO/)
- RYLR998 LoRa Module
- TP4056 battery charging module
- MG90S servo
- RGB Neopixel Jewel
- [DC to DC boost converter](https://www.amazon.com/DAOKI-Converter-Step-Up-Voltage-Regulator/dp/B08M19C7MM?crid=2Z80V26U1QVNL&dib=eyJ2IjoiMSJ9.Qu6yC0sr46xT-JAlyuJRzMTYiKvKh89AE1XABqWGHhNNgBk0eLLyxLVy9oL219KJTXiAPqcuAmJJ_WomyVOTeuR1RlZMRXPUkYm49GQhe_heYbUgc3ksa3DgdwdUgDHIkLuI8o_-suwRAgCDIW5fUdif0F6P_ClVGuPOfintIyflluvBdzqBDDhdwKS39F16DTimaVabgTgv5oC3Ph8CAgFVraVQrbnluZtHHfov88TOu8oDAoefKvEQsJ80pV3HnhjWI6ngREmsI00DgFXexjPBbMHlJWpUKmtKHKJK4cw.zKg7F-Nb-AHJbabyyR5hGbe-BdNrHKMpqnqtsgKUoBs&dib_tag=se&keywords=5PCS+Mini+DC-DC+Boost+Converter+Module+3V+3.2V+3.3V+3.7V+5V+daoki&qid=1749086221&s=industrial&sprefix=5pcs+mini+dc-dc+boost+converter+module+3v+3.2v+3.3v+3.7v+5v+daoki%2Cindustrial%2C88&sr=1-1)
- [LiPo battery](https://www.amazon.com/MakerHawk-Rechargeable-Protection-Insulated-Development/dp/B0D3LQYX49?crid=1K4DD4ZHQ2VU&dib=eyJ2IjoiMSJ9.G9aP9TyJvjZBgUriALDk29xUXo27E5d8WCr3MoXgE4bsmJiwRk4wo4RiBkay8IykeUrdLTh6KfdLOtc9XFipuJQbsI1T5zSHNV-EwGU0c3DpY6Bm33SdK4NB71gpHLIhRpkZoV9u5NrZOZ1CURmF0qXFqY1KwC6xh4Re4-CAZoz1vOCPvA-m8RfAh2UvqV_pub_kO9XaWJ-FlOnbBVRG3KS03gWG304gZnPwuOFUQ-6ws8WtNLfDtoDQIotgizby0c4bKDhc0kl8lg_yBS2QfsKIigYtcKHT42n9DWKmRHo.vYT9wqxEeYm3QDWNJO025HJYn5YICWZT0Y32thY9txk&dib_tag=se&keywords=3.7v%2Blipo%2Bbattery%2B2200%2BmAh&qid=1749089366&s=electronics&sprefix=3.7v%2Blipo%2Bbattery%2B2200%2Bmah%2Celectronics%2C112&sr=1-3&th=1)
- [Digital logic converter](https://www.amazon.com/HiLetgo-Channels-Converter-Bi-Directional-3-3V-5V/dp/B07F7W91LC?dib=eyJ2IjoiMSJ9.TqJrQIEBEbX7U7-p-JXMtot7qk-d2R3iy6-ft_7cqKVjsitywtM507CSkx-iBJYruMYBBRdKk_EqBEWVXMcE-ZG0ObN6i_4276lUMBv90DqiQZpjoEaMH03OAT-GopwVXZxK2KbWCKEEgcjITcCb5GDpg47eDJICTyV3Oz94jA2f8lle--WZZH1dWgZ6AUC-tonyFv3-zcr-RyT_jxQOatYUfFmL4U-Noss5ZeCVoSo._Yw2--RAlmwcyBRwYUqSSJBe-sBoGEjMQcbOkXBi5x4&dib_tag=se&keywords=3.3v+5v+logic+level+converter&qid=1749501269&sr=8-3)


**prats server side**
- USB to TTL Serial cable
- a RYLR998 LoRa module



#### **Notes on RYRL998:**
the thing comes pre programmed to be controlled with AT commands, [see detailed documentation here](https://reyax.com/upload/products_download/download_file/LoRa_AT_Command_RYLR998_RYLR498_EN.pdf). The RYLR needs to be interfaced with via sending the AT commands to it via serial

Quick notes:<br>
Module ids range 1-65535. 0 address cannot be addressed individually, all communication sent to address 0 is sent to all nodes. I have programmed the system in a way where 65535 id belongs to the LoRa module connected to QLAB_maincomputer. The maximum length of a message that can be sent over LoRa is 240 ascii characters, with the ability to send a few messages a second. 

<br>

# Software documentation 
All the files running server side - on the QLAB_maincomputer - are located in the `server folder`, all of the ones running locally on each node are in the `client folder` of this repo


## Server side
**To start the server:** 
1. open terminal and plug in the LoRa module 
2. run `ls /dev/tty.*`  to check the list of available ports, the one you are looking for will look something like `/dev/tty.usbserial-XX` (idk why yet but the port number changes every time you plug the module in)
3. open `lightserver.py` and replace `port = '/dev/tty.usbserial-XX'` on line 13 with the LoRa module port
4. in the terminal navigate to the directory where you placed the contents of the `server` folder
5. make `runme.sh` executable via running `chmod +x runme.sh`, then 
then execute it with `./runme.sh`
<br>

### runme.sh
This is a bash script that sets up the virtual python environment, installs all of the external modules that are needed for the server to function, then runs `lightserver.py` The script needs an internet connection ro run (at least for the first time) in order to download the modules.

### lgihtserver.py
where the python code for the actual server is. starts the server on localhost 127.0.0.1:8080 and gives access to REPL for debugging. to stop the server just kill the REPL with ctrl+D or `exit()`

### src/Mesh.py
Class to create objects of the network mesh. The mesh object would be a double nested list; so list of branches, where each branch is a list of node IDs in it. this means that the mesh structure would not be in any way connected to nominal IDs of the nodes, which will make it easier to manage and be able to restructure the mesh network topology if needed [WIP]

### src/utils.py
a place to put miscellaneous functions that help with programming/debugging 

### src/reyax.py 
A python adapted version of a [micropython RYLR998 driver](https://github.com/TimHanewich/MicroPython-Collection/blob/master/REYAX-RYLR998/reyax.py) i found [here](https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f)

### pyserialwrapper.py
the RYLR driver uses machine.UART module which is not for standard python. this wrapper class to makes it so the RYLR998 driver is compatible with the pyserial module that is used instead 


## Client side

### src/reyax.py 
[micropython RYLR998 driver](https://github.com/TimHanewich/MicroPython-Collection/blob/master/REYAX-RYLR998/reyax.py) i found [here](https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f)

### src/utils.py 
functions that help with programming. this is where the animation rendering functions and the functions that control hardware (motor, leds, setting up the rylr) are defined

### boot.py
runs on startup.

there are three processes that need to be dealt with concurrently/cooperatively - LoRa polling (must process servers messages near instantly), animation rendering (must be interrupt-able even mid animation, and animations need to loop), and REPL/usb serial for debug and reprogramming. Currently attempting to have animation rendering and usb serial/repl handled with uasyncio on core 0 and lora polling on thread 2 (failing).

currently uses _thread module to have `listen_to_host()` function run indefinitely on the second core - thats because the method uses serial to poll the lora module for incoming server messages, and even though the module is initialized with picos uart1 (see `connection_setup()` in `utils.py`), in my previous testing i found that it still blocks the usb serial, meaning reprogramming and access to repl is impossible if run on core 0. I looked it up, and the second thread does actually run on the second core with the same py interpreter, meaning blocking processes on core 1 do not affect core 0 with the usb serial and repl. core 1 is unable to run uasyncio as it is neither heap nor thread safe. 

