#for detailed breakdown reference https://www.youtube.com/watch?v=eEBUl07-ub4 for servo control and
#https://toptechboy.com/controlling-neopixel-array-on-pio-state-machine-on-raspberry-pi-pico/ for neopixels

import machine
import rp2
from rp2 import StateMachine
import time

rp2.PIO(0).remove_program() #here we will make it so the programmable memory of the state machine is getting
#rp2.PIO(1).remove_program()
#cleared out on every restart, as it is not done so automatically which leads to running out of memory

#SERVO ASSEMBLY - as a result of testing, the prevoius method of contorllign hte servo was ebtter timingwise
#taking 1~ 200 ns (uncomment to test) while, because of sm0.exec("pull()") the pio way takes ~46000

# servo = machine.PWM(machine.Pin(17))
# servo.freq(50)  # 50Hz for servo control
# servo_last_angle = 180

# def servo_set_angle(angle):
#     t_st = time.ticks_cpu()
#     # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
#     min_duty = 1638  # 1ms pulse (5% of 20ms)
#     max_duty = 8192  # 2ms pulse (10% of 20ms)
#     duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
#     servo.duty_u16(duty)
    
#     t_e = time.ticks_cpu()
#     print(f'it took {str(t_e-t_st)} cpu clock cycles at ~200mHz being approx {str(((t_e-t_st)/200000)*1000000)} nanoseconds to set serbvo angle')

#this pio will run continiously, holding the signal based on what ends up being pulled into the ISR
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def servo_set_pio():
    #set values to scratch registers then move in to the ISR 5 bits at a time (the max amount of bits mov can operate on)
    #this is the pulse width value - the one that will be controlling the servo angle, here it is 1500, so 90 deg
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
    in_(y, 5) #value in ISR now 100111000100000 bin - 20000 dec - the servos period
    
    wrap_target()
    #update scratch registers
    mov(x,osr) 
    mov(y, isr)
    
    set(pins, 0) #start low pulse
    label('periodloop')
    jmp(x_not_y, 'todecjump')#if x!= y jump to decrementing jump, if not continiue execution
    set(pins, 1) #start high signal
    label('todecjump')
    jmp(y_dec,'periodloop')#decrement y (pulse period) and restart the loop, as y is 2000
    #it will execute counting loop 2000 time giving the full period before wrapping
    
    wrap()


sm0 = rp2.StateMachine(0, servo_set_pio, freq=2000000, set_base=machine.Pin(17))
#reference the period loop of the PIO programm. there are two instructions (except for the
#singular loop where x = y, tehre are 3 there but we will ignore it and assume it to be within
#the margin of error) being executed per loop, those being the jump statements, thus in order
#for 1 iteration to take 1ms we will have to have 1 instruction take 0.5ms, so we will be 
#setting the frequency for the state machine at 2000000
sm0.active(1)
#servo now should rotate to 90

time.sleep(1)

sm0.put(2500) #put 2500 in FIFO tx register - this will not turn the servo as the pio is generating
#pwm based on what is in the ISR - so whatever is in the tx fifo needs to first be pulled into isr

#this will be done with the following - making python execute a state machine assembly pull command
#what is nice about it is that it will execute it no matter which part of the loop the pio is in
#and also will not interefere with the timining like it would have if weve done it within pio
sm0.exec("pull()")#the servo now shoul rotate to 180


def set_angle_servo(angle): #fun fact when you set it to 190 it starts spinning continiuously with a 360 range
    t_st = time.ticks_cpu()
    
    angle = 500+int(angle*11.11)#convert angle to 500-2500 range
    sm0.put(angle)
    t_p = time.ticks_cpu()
    sm0.exec("pull()") #this is taking too long TODO: fix in some way 
    
    t_e = time.ticks_cpu()
    print(f'it took {str(t_p-t_st)} cpu clock cycles at ~200mHz being approx {str(((t_p-t_st)/200000)*1000000)} nanoseconds to put the agnle in the FIFO')
    print(f'''it took {str(t_e-t_st)} cpu clock cycles at ~200mHz being approx {str(((t_e-t_st)/200000)*1000000)} nanoseconds
    to preform the whole adressign including telling the state machine to execute pull()''')


# counter = 500
# timer_servo = machine.Timer()#an easy out is to use a timer, it is already async
# def timer_callback(timer):
#     global counter
#     if counter < 2499:
#         sm0.put(counter)
#         sm0.exec("pull()")
#         counter += 20
#i will set the period here to 30 jsut to make sure the pwm has time to finish fully
# timer_servo.init(period=30, mode=machine.Timer.PERIODIC, callback=timer_callback)
# timer_servo.deinit()




#NEOPIXELS ASSEMBLY
#here the sideset pin will be the np data in order to set pins in parallel withe executing instructions
#set autopull to true so that when rx fifo has 24 bits (1 pixel color data) it is pulled in automatically 
#and python does not have to constantly put 
#neopixels operate at 800mhz that is a signal period of 1.25 msec. were gonna operate
#the machine at 10 times faster to have 10 cock cycles per period so 8,000,000 hz
#6 high and 4 low cycles for a 1 bit, 3 high and 7 low for a 0 bit
#each color 0-255 color value is an 8bit number so we are going to have 24 bits per pixel adressing
#so 24x7 = 168 to update the whole jewel
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

sm4 = rp2.StateMachine(4, jewel_set_pio, freq=8000000, sideset_base=machine.Pin(16))#use the fifth state machine so that
#the machines are on different blocks and do not share one block's 32 word memory
sm4.active(1)

def set_all_pixels(colors):
    t_st = time.ticks_cpu()
    colors.insert(0, [0,0,0])#TODO: i dont know why but there is an offset of 1 list item eg it is as if there is an
    #additional led that is taking off the first 24 bits of the train for some reason 
    for color in colors:
        grb=color[1]<<16 | color[0]<<8 | color[2]#neopixels expect green FIRST then red then blue
        sm4.put(grb, 8) 
    t_e = time.ticks_cpu()
    print(f'it took {str(t_e-t_st)} cpu clock cycles at ~200mHz being approx {str(((t_e-t_st)/200000)*1000000)} nanoseconds to set all of the leds')
 