import rp2
import machine  # type:ignore
import time

#ight lets start reworking the logic
# PIO clock will run at 1 MHz → 1 tick = 1 µs
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def servo_pwm():
    pull(noblock)             .side(0)     # Get high time in us (from FIFO)
    mov(x, osr)               .side(0)     # Move to X register
    set(pins, 1)              .side(1)     # Set pin high
    label("delay_high")
    nop()                     .side(1)
    jmp(x_dec, "delay_high")  .side(1)     # Wait high time
    set(pins, 0)              .side(0)     # Set pin low
    set(x, 20000)             .side(0)     # 20ms total period (in us)
    label("delay_low")
    nop()                     .side(0)
    jmp(x_dec, "delay_low")   .side(0)     # Wait remaining period


servo_pin =machine.Pin(17, machine.Pin.OUT)
state_machine = rp2.StateMachine(0, servo_pwm, freq=1_000_000, sideset_base=servo_pin)
#above args are state machine id 0, servo_pwm pio program defined above, 1MHz = 1us resolution, servos pwm pin to be controlled by the machine
state_machine.activate(0)
servo_last_angle = 180


def __angle_to_pulse(angle):
        # Clamp angle
        angle = max(0, min(180, angle))
        # Convert angle to microseconds: 0° = 1000us, 180° = 2000us
        return int(1000 + (angle / 180) * 1000)

def set_angle(angle):
        state_machine.put(__angle_to_pulse(angle))



#were gonna prentend the below doesnt exist for now
def servo_test():    
    for angle in range(0, 181, 30):
        servo_set_angle(angle)
        time.sleep(0.1)
    for angle in range(180, -1, -30):
        servo_set_angle(angle)
        time.sleep(0.1)
    print('motor test')


#TODO: percentage impl. use 40 as a placeholder for now
def servo_set_angle(angle):
    # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
    min_duty = 1638  # 1ms pulse (5% of 20ms)
    max_duty = 8192  # 2ms pulse (10% of 20ms)
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)


#TODO: percentage impl. use 40 as a placeholder for now
def servo_rotate(to_angle, speed = 0.01):
    """ARGS > to_angle:int, speed:int (optional wait time between steps in seconds; 0.01 by default)"""
    global servo_last_angle
    print('> Rotating form', servo_last_angle, 'to', to_angle)
    if to_angle > servo_last_angle:
        for deg in range(servo_last_angle, to_angle):
            servo_set_angle(deg)
            time.sleep(speed)
    else:
        for deg in range(servo_last_angle, to_angle, -1):
            servo_set_angle(deg)
            time.sleep(speed)
    servo_last_angle = to_angle
    print('rotated')