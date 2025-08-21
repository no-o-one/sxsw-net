import src.animationutils as animationutils
try:
    import src.jewelutils as jewelutils
except:
    print("!couldnt import jewelutils.py from src!")
try:
    import src.servoutils as servoutils
except:
    print("!couldnt import servoutils.py from src!")


this_servo = servoutils.Servo()
this_jewel = jewelutils.Neopixel()


#Example animations
animstep_example_s1 = animationutils.AnimationInstance(this_servo, 'linear', 1, 100, 0, 90)
animstep_example_s2 = animationutils.AnimationInstance(this_servo, 'bounce', 2, 100, 90, 180)
animstep_example_s3 = animationutils.AnimationInstance(this_servo, 'cubic_out', 1, 100, 180, 1)
example_anim_servo = animationutils.AnimationController([animstep_example_s1, animstep_example_s2, animstep_example_s3])

animstep_example_j1 = animationutils.AnimationInstance(this_jewel, 'bounce', 1.5, 100, 1, 100)
animstep_example_j2 = animationutils.AnimationInstance(this_jewel, 'cubic_out', 1, 100, 100, 1) 
example_anim_jewel = animationutils.AnimationController([animstep_example_j1, animstep_example_j2])

#dystopia
servo_dystopia = animationutils.AnimationController([
    animationutils.AnimationInstance(this_servo, 'linear', 0.1, 120, 90, 120),
    animationutils.AnimationInstance(this_servo, 'linear', 0.05, 120, 120, 40),
    animationutils.AnimationInstance(this_servo, 'linear', 0.08, 120, 40, 170),
    animationutils.AnimationInstance(this_servo, 'bounce', 0.1, 120, 170, 20),
    animationutils.AnimationInstance(this_servo, 'quint_out', 0.12, 120, 20, 90),
] )

jewel_dystopia = animationutils.AnimationController([
    animationutils.AnimationInstance(this_jewel, 'linear', 0.1, 100, 0, 255),   # flash
    animationutils.AnimationInstance(this_jewel, 'linear', 0.05, 100, 255, 0),
    animationutils.AnimationInstance(this_jewel, 'quint_in', 0.1, 100, 0, 180),
    animationutils.AnimationInstance(this_jewel, 'quint_out', 0.05, 100, 180, 0),
] )

#spotlights
servo_spotlight = animationutils.AnimationController([
    animationutils.AnimationInstance(this_servo, 'quint_in', 0.2, 100, 0, 45),
    animationutils.AnimationInstance(this_servo, 'quint_out', 0.1, 100, 45, 10),
    animationutils.AnimationInstance(this_servo, 'quint_in', 0.2, 100, 10, 70),
    animationutils.AnimationInstance(this_servo, 'quint_out', 0.1, 100, 70, 0),
] )

jewel_spotlight = animationutils.AnimationController([
    animationutils.AnimationInstance(this_jewel, 'quint_in_out', 0.1, 100, 0, 200),
    animationutils.AnimationInstance(this_jewel, 'linear', 0.05, 100, 200, 0),
    animationutils.AnimationInstance(this_jewel, 'linear', 0.2, 100, 0, 255),
    animationutils.AnimationInstance(this_jewel, 'quint_out', 0.1, 100, 255, 0),
] )

#test
servo_test = animationutils.AnimationController([
    animationutils.AnimationInstance(this_servo, 'linear', 1, 60, 0, 180),
    animationutils.AnimationInstance(this_servo, 'linear', 1, 60, 180, 0),
])

jewel_test = animationutils.AnimationController([
    animationutils.AnimationInstance(this_jewel, 'linear', 0.8, 60, 0, 255),  # R up
    animationutils.AnimationInstance(this_jewel, 'linear', 0.8, 60, 255, 0),  # R down
    animationutils.AnimationInstance(this_jewel, 'linear', 0.8, 60, 0, 255),  # G up
    animationutils.AnimationInstance(this_jewel, 'linear', 0.8, 60, 255, 0),  # G down
    animationutils.AnimationInstance(this_jewel, 'linear', 0.8, 60, 0, 255),  # B up
    animationutils.AnimationInstance(this_jewel, 'linear', 0.8, 60, 255, 0),  # B down
])

#irl
servo_irl = animationutils.AnimationController([
    animationutils.AnimationInstance(this_servo, 'cubic_in_out', 2.5, 100, 10, 40),
    animationutils.AnimationInstance(this_servo, 'cubic_out', 2, 100, 40, 20),
    animationutils.AnimationInstance(this_servo, 'cubic_in', 2.5, 100, 20, 10),
] )

jewel_irl = animationutils.AnimationController([
    animationutils.AnimationInstance(this_jewel, 'cubic_in_out', 3, 100, 30, 120),  # pulse up
    animationutils.AnimationInstance(this_jewel, 'cubic_out', 2.5, 100, 120, 60),   # fade back
    animationutils.AnimationInstance(this_jewel, 'cubic_in', 2.5, 100, 60, 30),
] )

#nature
servo_nature = animationutils.AnimationController([
    animationutils.AnimationInstance(this_servo, 'cubic_in_out', 2.5, 60, 50, 70),
    animationutils.AnimationInstance(this_servo, 'cubic_out', 2, 60, 70, 55),
    animationutils.AnimationInstance(this_servo, 'cubic_in', 2.2, 60, 55, 65),
    animationutils.AnimationInstance(this_servo, 'cubic_out', 2.3, 60, 65, 50),
] )

jewel_nature = animationutils.AnimationController([
    animationutils.AnimationInstance(this_jewel, 'cubic_in_out', 3, 100, 30, 80),   # soft pastel fade
    animationutils.AnimationInstance(this_jewel, 'cubic_out', 2.5, 100, 80, 40),
    animationutils.AnimationInstance(this_jewel, 'cubic_in', 2.5, 100, 40, 60),
] )

