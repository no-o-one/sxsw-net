import machine  # type:ignore

class Servo():
    #TODO: implement @property and checks
    def __init__(self, pwm_pin=17, last_angle=180):
        '''ARGS>  pwm_pin:int, last_angle:int'''
        self.pwm_pin = machine.PWM(machine.Pin(pwm_pin))
        self.pwm_pin.freq(50) # 50Hz for servo control
        self.last_angle = last_angle

    def set_angle(self, angle):
        # Convert angle (0–180) to duty_u16 value (~1638 to 8192)
        min_duty = 1638  # 1ms pulse (5% of 20ms)
        max_duty = 8192  # 2ms pulse (10% of 20ms)
        duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
        self.pwm_pin.duty_u16(duty)



# def servo_test():    
#     for angle in range(0, 181, 30):
#         servo_set_angle(angle)
#         time.sleep(0.1)
#     for angle in range(180, -1, -30):
#         servo_set_angle(angle)
#         time.sleep(0.1)
#     print('motor test')


# #TODO: percentage impl. use 40 as a placeholder for now
# def servo_rotate(to_angle, speed = 0.01):
#     """ARGS > to_angle:int, speed:int (optional wait time between steps in seconds; 0.01 by default)"""
#     global servo_last_angle
#     print('> Rotating form', servo_last_angle, 'to', to_angle)
#     if to_angle > servo_last_angle:
#         for deg in range(servo_last_angle, to_angle):
#             servo_set_angle(deg)
#             time.sleep(speed)
#     else:
#         for deg in range(servo_last_angle, to_angle, -1):
#             servo_set_angle(deg)
#             time.sleep(speed)
#     servo_last_angle = to_angle
#     print('rotated')