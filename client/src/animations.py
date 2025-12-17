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

#spotlights
servo_spotlight =  AnimationController([
     AnimationInstance(this_servo, 'quint_in', 0.2, 100, 0, 45),
     AnimationInstance(this_servo, 'quint_out', 0.1, 100, 45, 10),
     AnimationInstance(this_servo, 'quint_in', 0.2, 100, 10, 70),
     AnimationInstance(this_servo, 'quint_out', 0.1, 100, 70, 0),
] )

jewel_spotlight =  AnimationController([
     AnimationInstance(this_jewel, 'quint_in_out', 0.1, 100, 0, 200),
     AnimationInstance(this_jewel, 'linear', 0.05, 100, 200, 0),
     AnimationInstance(this_jewel, 'linear', 0.2, 100, 0, 255),
     AnimationInstance(this_jewel, 'quint_out', 0.1, 100, 255, 0),
] )

#test
servo_test =  AnimationController([
     AnimationInstance(this_servo, 'linear', 1, 60, 0, 180),
     AnimationInstance(this_servo, 'linear', 1, 60, 180, 0),
])

jewel_test =  AnimationController([
     AnimationInstance(this_jewel, 'linear', 0.8, 60, 0, 255),  # R up
     AnimationInstance(this_jewel, 'linear', 0.8, 60, 255, 0),  # R down
     AnimationInstance(this_jewel, 'linear', 0.8, 60, 0, 255),  # G up
     AnimationInstance(this_jewel, 'linear', 0.8, 60, 255, 0),  # G down
     AnimationInstance(this_jewel, 'linear', 0.8, 60, 0, 255),  # B up
     AnimationInstance(this_jewel, 'linear', 0.8, 60, 255, 0),  # B down
])

#irl
servo_irl =  AnimationController([
     AnimationInstance(this_servo, 'cubic_in_out', 2.5, 100, 10, 40),
     AnimationInstance(this_servo, 'cubic_out', 2, 100, 40, 20),
     AnimationInstance(this_servo, 'cubic_in', 2.5, 100, 20, 10),
] )

jewel_irl =  AnimationController([
     AnimationInstance(this_jewel, 'cubic_in_out', 3, 100, 30, 120),  # pulse up
     AnimationInstance(this_jewel, 'cubic_out', 2.5, 100, 120, 60),   # fade back
     AnimationInstance(this_jewel, 'cubic_in', 2.5, 100, 60, 30),
] )

#nature
servo_nature =  AnimationController([
     AnimationInstance(this_servo, 'cubic_in_out', 2.5, 60, 50, 70),
     AnimationInstance(this_servo, 'cubic_out', 2, 60, 70, 55),
     AnimationInstance(this_servo, 'cubic_in', 2.2, 60, 55, 65),
     AnimationInstance(this_servo, 'cubic_out', 2.3, 60, 65, 50),
] )

jewel_nature =  AnimationController([
     AnimationInstance(this_jewel, 'cubic_in_out', 3, 100, 30, 80),   # soft pastel fade
     AnimationInstance(this_jewel, 'cubic_out', 2.5, 100, 80, 40),
     AnimationInstance(this_jewel, 'cubic_in', 2.5, 100, 40, 60),
] )
servo_open_flower =  AnimationController([
     AnimationInstance(this_servo, 'quint_out', 4 , 100, 15, 165)
], False)
servo_close_flower =  AnimationController([
     AnimationInstance(this_servo, 'quint_in', 4 , 100, 165, 15)
], False)
servo_bloom1_flower =  AnimationController([ AnimationInstance(this_servo, 'quint_in_out', 3, 100, 15, 45)], False)
servo_bloom2_flower =  AnimationController([ AnimationInstance(this_servo, 'cubic_out', 2, 100, 45, 135)], False)
servo_bloom3_flower =  AnimationController([ AnimationInstance(this_servo, 'quint_in_out', 3 , 100, 135, 165)], False)


j_bloom_pink =  AnimationController([ AnimationInstance(this_jewel, 'cubic_in', 2.5, 100, [120,10,50], [10,0,120]),
                                                   AnimationInstance(this_jewel, 'cubic_out', 4, 100, [10,0,120], [80,10,90]),
                                                   AnimationInstance(this_jewel, 'cubic_in_out', 5, 100, [80,10,90], [80,50,0]),
                                                   AnimationInstance(this_jewel, 'cubic_in_out', 4, 100, [80,50,0], [120,10,80]),
                                                   AnimationInstance(this_jewel, 'cubic_in', 3, 100, [120,10,80], [120,10,50]),
                                                  ], True)
j_bloom_pink_litup =  AnimationController([ AnimationInstance(this_jewel, 'cubic_in', 3, 100, [0,0,0], [120,10,60])], False)

j_bloom_whgreen =  AnimationController([ AnimationInstance(this_jewel, 'quint_in_out', 1.5, 100, [10,10,10], [50,50,50]),
                                                   AnimationInstance(this_jewel, 'bounce', 5, 100, [50,50,50], [30,65,5]),
                                                   AnimationInstance(this_jewel, 'cubic_in', 4, 100, [30,65,5], [50, 50, 10]),
                                                   AnimationInstance(this_jewel, 'quint_out', 4, 100, [50, 50, 10], [25, 25, 25]),
                                                   AnimationInstance(this_jewel, 'cubic_in', 2, 100, [25, 25, 25], [40,40,60]),
                                                   AnimationInstance(this_jewel, 'cubic_out', 4, 100, [50,50,50], [10,10,10]),
                                                  ], True)

j_bloom_warmup =  AnimationController([ AnimationInstance(this_jewel, 'cubic_in_out', 8, 300, [0,0,0], [25, 15, 3]),
                                                   AnimationInstance(this_jewel, 'cubic_in_out', 6, 300, [25, 15, 3], [60, 15, 0]),
                                                   AnimationInstance(this_jewel, 'cubic_in_out', 6, 100, [60, 15, 0], [75, 9, 1])
#                                                    AnimationInstance(this_jewel, 'quint_out', 4, 100, [50, 50, 10], [25, 25, 25]),
#                                                    AnimationInstance(this_jewel, 'cubic_in', 2, 100, [25, 25, 25], [40,40,60]),
#                                                    AnimationInstance(this_jewel, 'cubic_out', 4, 100, [50,50,50], [10,10,10]),
                                                  ], False)
j_bloom_warmup_die =  AnimationController([ AnimationInstance(this_jewel, 'bounce', 3, 300, [75, 9, 1], [0,0,0])
                                                  ], False)


soft_open_late =  AnimationController([ AnimationInstance(this_servo, 'quint_out', 3, 60, 100, 165)], False)
soft_open_late_loop =  AnimationController([ AnimationInstance(this_servo, 'quint_out', 3, 60, 100, 135),
                                                          AnimationInstance(this_servo, 'quint_out', 3, 60, 135, 165),
                                                          AnimationInstance(this_servo, 'quint_out', 3, 60, 165, 120),
                                                          AnimationInstance(this_servo, 'quint_out', 3, 60, 120, 100)], True)

s_warmup_open =  AnimationController([ AnimationInstance(this_servo, 'quint_in_out', 3, 60, 15, 100)], False)

s_warmup_close =  AnimationController([ AnimationInstance(this_servo, 'quint_in', 1, 60, 80, 0)], False)

s_open_more =  AnimationController([ AnimationInstance(this_servo, 'quint_out', 4, 60, 100, 165)], False)
j_transit =  AnimationController([  AnimationInstance(this_jewel, 'cubic_out', 1, 100, [75, 9 ,1], [159, 0, 80])
                                                  ], False)


j_open_more =  AnimationController([ AnimationInstance(this_jewel, 'cubic_out', 4, 100, [159,0, 80], [0, 0, 200]),
                                                   AnimationInstance(this_jewel, 'cubic_in_out', 5, 100, [0, 0, 200], [255, 0, 0 ]),
                                                   AnimationInstance(this_jewel, 'cubic_in_out', 4, 100, [255, 0, 0 ], [0, 255, 17]),
                                                   AnimationInstance(this_jewel, 'cubic_in', 3, 100, [0, 255, 17], [159,0, 80]),
                                                  ], True)


servo_bloom =  AnimationController([ AnimationInstance(this_servo, 'quint_in_out', 4, 100, 15, 95),
                                                   AnimationInstance(this_servo, 'quint_out', 4, 100, 95, 165)], False)
    


    
