# Client side docs


## **src.animationutils.AnimationInstance**

Class controlling preipherals, animating between two set keyframes. Triggers `.set()` of the peripheral object in order to trigger hardware changes. Timing frame switches is implemented with virtual timers in order to be non blocking.

### Constructor
| Arguments    | Type   | Default Value | Role                          |
|-----------|--------|------------|---------------|
| peripheral    | Servo/Neopixel class object     | *argument required* | peripheral object to be animated |
| curve   | String | 'linear'    | motion curve fo the animation
| length  | int  | *argument required*    | length of the animation in seconds |
|fps|int|*argument required*|frames per second for the animation|
|start_keyframe| int degrees 0-180, int brightness 0-255, or a list [R,G,B]| *argument required*|start keyframe
|end_keyframe| int degrees 0-180, int brightness 0-255, or a list [R,G,B]| *argument required* |end keyframe

### play()
Plays the animation - inits a timer that triggers `.set()`s  for the peripheral objects

| Arguments    | Type   | Default Value | Role                          |
|-------------|--------|---------------|---------------|
| called_by_controller   | AnimationController obj | None | used for tracking current and the next queued AnimationInstances |

### kill()
Stops the animation - deinits the animation's timer, so all following frames are not rendered

### Classmethod get_instances()
Returns a list of all AnimationInstance objects created

### Classmethod kill_all()
Gets all instances of the class created then deinits all their timers 

<br>


## **src.animationutils.AnimationController**
Class queueing and managing `AnimationInstance` objects to create 

### Constructor

| Arguments    | Type   | Default Value | Role                          |
|-----------|--------|------------|---------------|
| sequence    | list of AnimationInstance objects    | *argument required* | stores the sequence of animations to be played one after another |
| is_looping   | Boolean | True    | If True, the animation sequence will be played repeatedly until killed, if False, it will be played only once

#### play()
Plays the animation sequence - calls `.play()` on the first Instance in the sequence, which triggers the rest within the timer callback


### kill()
Stops the animation - deinits the current Instance's timer, so all following frames and AnimationInstances are not rendered

### Classmethod get_instances()
Returns a list of all AnimationController objects created

### Classmethod kill_all()
Gets all instances of the class created then deinits all the individual AnimationInstance timers, thus the call to move to the next animation in the sequence also never happens


















reyax fucntions 

create_rylr(self_address: int) -> RYLR998:
first creates a machine.UART object on tx pin4 and rx pin 5 with 115200 baudrate, then creates a rylr (a RYLR998 class object) with the uart object created. sets the adress of that to the oe provided in the args(uses set_address() class method). preforms rylr.ping(). sends a connection notice to the central module 

safe_create_rylr(id, max_retries=5)
preforms create_rylr 5 times by default, or if set otherwise, max_treis times until succeeds or runs out of attempts


rylr object fucntions

ping()
sends an "AT\r\n" to the lora module, returns true if responed "+OK\r\n", flas e if otherwise

_collect_rx(self)
reads the uart rx channel, then adds it to the python objects internal buffer var(the object is a bytes array)

animation syntax AnimationController([lsit fo naimation instances to be played one after another])



full setup file system
'boot.py', 'reyax.py', 'utils.py', 'jewelutils.py', 'servoutils.py', 'animationutils.py', 'animations.py'



