try:
    from src.animationutils import *
except:
    print("!err from animations: couldnt import animationutils!")

#PERIPHERAL INITS
this_servo = Servo()
this_jewel = Neopixel()


#Example animations
animstep_example_s1 =  AnimationInstance(this_servo, 'linear', 1, 100, 0, 90)
animstep_example_s2 =  AnimationInstance(this_servo, 'bounce', 2, 100, 90, 180)
animstep_example_s3 =  AnimationInstance(this_servo, 'cubic_out', 1, 100, 180, 1)
example_anim_servo =  AnimationController([animstep_example_s1, animstep_example_s2, animstep_example_s3])

animstep_example_j1 =  AnimationInstance(this_jewel, 'bounce', 1.5, 100, 1, 100)
animstep_example_j2 =  AnimationInstance(this_jewel, 'cubic_out', 1, 100, 100, 1) 
example_anim_jewel =  AnimationController([animstep_example_j1, animstep_example_j2])

#dystopia
servo_dystopia =  AnimationController([
     AnimationInstance(this_servo, 'linear', 0.1, 120, 90, 120),
     AnimationInstance(this_servo, 'linear', 0.05, 120, 120, 40),
     AnimationInstance(this_servo, 'linear', 0.08, 120, 40, 170),
     AnimationInstance(this_servo, 'bounce', 0.1, 120, 170, 20),
     AnimationInstance(this_servo, 'quint_out', 0.12, 120, 20, 90),
] )

jewel_dystopia =  AnimationController([
     AnimationInstance(this_jewel, 'linear', 0.1, 100, 0, 255),   # flash
     AnimationInstance(this_jewel, 'linear', 0.05, 100, 255, 0),
     AnimationInstance(this_jewel, 'quint_in', 0.1, 100, 0, 180),
     AnimationInstance(this_jewel, 'quint_out', 0.05, 100, 180, 0),
] )


    
