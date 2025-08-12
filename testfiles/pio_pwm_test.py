import machine
import rp2
from rp2 import StateMachine
import time

rp2.PIO(0).remove_program()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def servo_set_pio():
    #set values to scratch registers then move in to the ISR 5 bits at a time (the max amount of bits mov can operate on)
    #this is the pulse width value - the one that will be controlling the servo angle, here it is 1500 ms, so 90 deg
    set(x, 0b10111)
    in_(x, 5)
    set(x, 0b01110)
    in_(x, 5)
    set(x, 0b00000)
    in_(x, 1) #value in ISR now bin 10111011100 -1500 dec
    mov(osr, isr) #move into the OSR to store 
    
    mov(isr, null) #clear out ISR before populating with the period
    set(y, 0b10011)
    in_(y, 5)
    set(y, 0b10001)
    in_(y, 5)
    set(y, 0b00000)
    in_(y, 5) #value in ISR now 100111000100000 bin - 2000 dec - the servos period
    
    wrap_target()
    #update scratch registers
    mov(x,osr) 
    mov(y, isr)
    
    set(pins, 0) #start low pulse
    label('periodloop')
    jmp(x_not_y, 'todecjump')#if x!= y jump to decrementing jump, if not continiue execution
    set(pins, 1) #start high signal
    label('todecjump')
    jmp(y_dec,'periodloop')#decrement y (pulse period) and restart the loop, as y is 2000 it will execute counting loop 2000 time giving the full period before wrapping
    
    wrap()


sm0 = rp2.StateMachine(0, servo_set_pio, freq=2000000, set_base=machine.Pin(17))
#reference the period loop of the PIO programm. there are two instructions (except for the singular loop where x = y, tehre are 3 there but we will
#ignore it and assume it to be within the margin of error) being executed per loop, those being the jump statements, thus in order for 1 iteration to
#take 1ms we will have to have 1 instruction take 0.5ms, so we will be setting the frequency for the state machine at 2000000
sm0.active(1)
#servo now should rotate to 90
