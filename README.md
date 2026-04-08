# Hardware documentation 

[pcb files!](https://drive.google.com/drive/folders/1o0MN87YVfZmZX_xxKThMRZH78RT8oLCC?usp=drive_link)

**parts client side**
- Non W Raspberry Pi pico with RP2040 flashed with [Micropython v1.125.0](https://micropython.org/download/RPI_PICO/)
- RYLR998 LoRa Module
- TP4056 battery charging module
- MG90S servo
- RGB Neopixel Jewel
- [buck-boost converter](https://www.digikey.com/en/products/detail/pololu/4085/16164508)
- 5000mah lipo battery
- [Digital logic converter](https://www.amazon.com/HiLetgo-Channels-Converter-Bi-Directional-3-3V-5V/dp/B07F7W91LC?dib=eyJ2IjoiMSJ9.TqJrQIEBEbX7U7-p-JXMtot7qk-d2R3iy6-ft_7cqKVjsitywtM507CSkx-iBJYruMYBBRdKk_EqBEWVXMcE-ZG0ObN6i_4276lUMBv90DqiQZpjoEaMH03OAT-GopwVXZxK2KbWCKEEgcjITcCb5GDpg47eDJICTyV3Oz94jA2f8lle--WZZH1dWgZ6AUC-tonyFv3-zcr-RyT_jxQOatYUfFmL4U-Noss5ZeCVoSo._Yw2--RAlmwcyBRwYUqSSJBe-sBoGEjMQcbOkXBi5x4&dib_tag=se&keywords=3.3v+5v+logic+level+converter&qid=1749501269&sr=8-3)
- [Gear's bearings x2](https://www.mcmaster.com/5909K12/)
- [Aligner's bearing](https://www.mcmaster.com/5905K528/)


**prats server side**
- USB to TTL Serial cable
- a RYLR998 LoRa module



#### **Notes on RYRL998:**
the thing comes pre programmed to be controlled with AT commands, [see detailed documentation here](https://reyax.com/upload/products_download/download_file/LoRa_AT_Command_RYLR998_RYLR498_EN.pdf). The RYLR needs to be interfaced with via sending the AT commands to it via serial

Quick notes:<br>
Module ids range 1-65535. 0 address cannot be addressed individually, all communication sent to address 0 is sent to all nodes. I have programmed the system in a way where 65535 id belongs to the LoRa module connected to QLAB_maincomputer. The maximum length of a message that can be sent over LoRa is 240 ascii characters, with the ability to send a few messages a second. 

<br>

# Software documentation <- needs an update in some places
> run `help(<thing_name>)` on functions, modules and objects to see what they do and what args they take - i should have a pretty good coverage in terms of documentation; Note: you can get the docstring of a class's constructor by running `help(<class_name>.__init__)`

All the files running server side - on the QLAB_maincomputer - are located in the `server folder`, all of the ones running locally on each node are in the `client folder` of this repo

#[THE FOLLOWING CAN BE SLIGHTLY OUTDATED]
## Server side
module listening logic is now implemented server side too

**To start the server:** 
run `server/server_flask.py` from terminal
<br>

### runme.sh
This is a bash script that sets up the virtual python environment, installs all of the external modules that are needed for the server to function, then runs `lightserver.py` The script needs an internet connection ro run (at least for the first time) in order to download the modules.

### lgihtserver.py
where the python code for the actual server is. starts the server on localhost 127.0.0.1:8080 and gives access to REPL for debugging. to stop the server just kill the REPL with ctrl+D or `exit()`

### src/Mesh.py
Class to create objects of the network mesh. The mesh object would be a double nested list; so list of branches, where each branch is a list of node IDs in it. this means that the mesh structure is not in any way connected to nominal IDs of the nodes

### src/utils.py
a place to put miscellaneous functions that help with programming/debugging 

### src/reyax.py 
This is a micropython driver for a RYRL998 with specifically non blocking functionality (safety precautions must be taken!!). it is now a fully rewritten different thing, but originally i used this [micropython RYLR998 driver](https://github.com/TimHanewich/MicroPython-Collection/blob/master/REYAX-RYLR998/reyax.py) i found [here](https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f), and this is the reference that i was using when writing the one in place now

### pyserialwrapper.py
the RYLR driver uses machine.UART module which is not for standard python. this wrapper class to makes it so the RYLR998 driver is compatible with the pyserial module that is used instead 


## Client side

### src/reyax.py 
This is a  client versoin of the micropython driver for a RYRL998 with specifically non blocking functionality (safety precautions must be taken!!). it is now a fully rewritten different thing, but originally i used this [micropython RYLR998 driver](https://github.com/TimHanewich/MicroPython-Collection/blob/master/REYAX-RYLR998/reyax.py) i found [here](https://timhanewich.medium.com/how-to-use-a-reyax-rylr998-lora-module-with-a-raspberry-pi-pico-and-other-microcontrollers-4ae52686836f), and this is the reference that i was using when writing the one in place now. The client version also has functionality added to retrieve the module's inbuilt id, as well as set the RF settings.


### src/jewelutils.py 
class for creating a neopixel object for controlling the jewel. here also the pio program that is used for async nopixel protocol generation is defined.

### src/servoutils.py 
class for creating a servo object for controlling the servo

### src/utils.py 
general utilities to be used in boot.py

### boot.py
runs on startup. listens to the host module on core 2. one core one tracks and controlls the animations and animation states.

### src/animationS.py
this is where the particular preset animations are defined using `animationutils.py` classes. these are then imported for use in boot.py

## ID system
to ensure constant module ids across reboots and reflashes, so that every physical node has a consistent id, i will make use of the fact that every lora module comes with a hard coded 12 byte UID. Upon startup module side each module will retrieve it and send it to the server. Server side there will be a lookup table that maps it to a short 1 byte (0-255) ID that will be used internally.

## Internal Protocol
upon satartup every node will send an ascii encoded string starting ("init [module UID]"); whe inquiring hte lora module, becuase it operates on the AT portocol all data it returns is ascii data. thus it is anyway easier to send this data over in the type it was recieved, and the fractions of a second tha that would be saved if i was to convert it to raw bits would not matter either way, as we dont really care about abos;utely minimising latency on the frew stratup processes that are rewuired (it is actually not clear fromt he documentation what type of data is the uid, but judgin by the fact that it is clearly defined as 12bytes, it then is probably a string represenation of a base16 (hex) encoding of the 12 byte UID)



### src/animationutils.py and animation logic
holds class `AnimationInstance` and `Animation Controller`
#### `AnimationIns
tance`
 establishes an instance of an animation (a singular curve), the curves shape and the means to control it via a virtual periodic timer so it runs async.
#### `AnimationController`
 creates a full animation object as a sequence of animation instances. this is so that animations can be complex and can contain multiple curves and be also controlled async. needs to be adapted to control the servo and the jewel at the same time

at this point then we will have to control jewel and servo async because they might have light and motion ainimations of different lengths


