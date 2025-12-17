documentation client side

reyax fucntions 

create_rylr(self_address: int) -> RYLR998:
first creates a machine.UART object on tx pin4 and rx pin 5 with 115200 baudrate, then creates a rylr (a RYLR998 class object) with the uart object created. sets the adress of that to the oe provided in the args(uses set_address() class method). preforms rylr.ping(). sends a connection notice to the central module 

safe_create_rylr(id, max_retries=5)
preforms create_rylr 5 times by default, or if set otherwise, max_treis times until succeeds or runs out of attempts


rylr object fucntions

ping()
sends an "AT\r\n" to the lora module, returns true if responed "+OK\r\n", flas e if otherwise

_collect_rx(self)
reads the uart rx channel, then adds it to the python objects internal buffer var(the object is a bytes array)

