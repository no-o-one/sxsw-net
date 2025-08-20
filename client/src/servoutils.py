import machine  # type:ignore

class Servo():
    #TODO: implement @property and checks
    def __init__(self, pwm_pin=17, last_angle=180):
        '''ARGS>  pwm_pin:int, last_angle:int'''
        self.pwm_pin = machine.PWM(machine.Pin(pwm_pin))
        self.pwm_pin.freq(50) # 50Hz for servo control
        self.last_angle = last_angle

    def set(self, angle):
        # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
        min_duty = 1638  # 1ms pulse (5% of 20ms)
        max_duty = 8192  # 2ms pulse (10% of 20ms)
        duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
        self.pwm_pin.duty_u16(duty)


