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

anim1 = animationutils.AnimationInstance(this_servo, 'linear', 1, 100, 0, 90)
anim2 = animationutils.AnimationInstance(this_servo, 'bounce', 2, 100, 90, 180)
anim3 = animationutils.AnimationInstance(this_servo, 'cubic_out', 1, 100, 180, 1)
anim4 = animationutils.AnimationInstance(this_jewel, 'bounce', 1.5, 100, 1, 100)
anim5 = animationutils.AnimationInstance(this_jewel, 'cubic_out', 1, 100, 100, 1) 

nature_animation = animationutils.AnimationController([anim1, anim2, anim3])
irl_animation = animationutils.AnimationController([anim4, anim5])
