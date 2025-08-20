import machine  # type:ignore
import rp2
import time

rp2.PIO(0).remove_program()

@rp2.asm_pio(sideset_init= rp2.PIO.OUT_HIGH, out_shiftdir= rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def jewel_set_pio(): #one instruction here will cost 1 clock cycle btw
    #when data is autopulled from tx fifo it ends up in osr so
    wrap_target()
    label("process_bit")
    out(x,1)    .side(0) #move one most significant bit form osr to x scratch register while setting
    #the pins to 0 as no matter whether the bit is a 0 or a 1 the signal always starts with low
    jmp(not_x, "is_zero_bit")     .side(1)#jump to logic 0 instructions if it is a 0, but in any case 
    #set pins to high as both logic 0 and 1 have a high signal following the low, the difference is in the 
    #duration of the high
    nop()     .side(1)[4]#set to high for one clock cycle and prolong for another 4 to get the full 6 high
    #cycles for a logic 1 together with the one on line 83
    nop()    .side(0)[3]#set the rest of the 10 cycle period to low (account for the low on the next line)
    jmp("process_bit")   .side(0)
    label("is_zero_bit")#process in case it is a logic 0 bit is the same as for the logic 1, but different lengths
    nop()     .side(1)[1]
    jmp("process_bit")  .side(0)[5]
    wrap()


class Neopixel():
    #TODO: implement @property and checks
    def __init__(self, data_pin=16, state_machine_id=0, pixels_amount=7):
        '''ARGS>  data_pin:int, state_machine_id:int, pixels_amount:int'''
        self.data_pin = machine.Pin(data_pin)
        self.state_machine_id = state_machine_id
        self.sm = rp2.StateMachine(self.state_machine_id, jewel_set_pio, freq=8000000, sideset_base=self.data_pin)
        self.sm.active(1)
        self.pixels_amount = pixels_amount

    def set(self, color):
        if isinstance(color, int):
            color = [color]*3
        if isinstance(color[0], int):
            color = [color]*self.pixels_amount   
        #color.insert(0, [0,0,0])#TODO: i dont know why but there is ?only sometimes? an offset of 1 list item eg it is as if there is an
        #additional led that is taking off the first 24 bits of the train for some reason 
        for c in color:
            grb=c[1]<<16 | c[0]<<8 | c[2]
            self.sm.put(grb, 8)
    
        
 
 


