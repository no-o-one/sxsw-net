try:
    from src.periphutils import *
except:
    print("!err from animationutils: couldnt import periphutils!")



current_animation_flag = 'none' #shared flag between the two threads
last_animation_flag = 'none'



class AnimationInstance():
    _instances = []  #List of all instances created, although prevents garbage collection

    @classmethod
    def get_instances(cls):
        '''Returns a list of all AnimationInstance objects created'''
        return cls._instances

    @classmethod
    def kill_all(cls):
        for instance in cls.get_instances():
            instance.timer.deinit()

    def __init__(self, peripheral, curve, length, fps, start_keyframe, end_keyframe):
        '''ARGS >
        
        peripheral - an object of a class Servo/Neopixel
        curve:str - options being 'cubic_in', 'cubic_out', cubic_in_out', 'quint_in', 'quint_out', 'quint_in_out', 'bounce', 'linear' 
        length:int - in seconds
        fps:int
        start_keyframe:int - start angle/color or a list [R,G,B]
        end_keyframe:int - end angle/color'''
        self.peripheral = peripheral
        self.curve = curve
        self.length = length
        self.fps = fps
        self.total_frames = self.length * self.fps #used for tracking current frames and calculating values with animation curves
        self.ms_between_frames = int(1000 / self.fps) #used for tracking current frames and calculating values with animation curves
        self.start_keyframe = start_keyframe 
        self.end_keyframe = end_keyframe 
        self.timer = machine.Timer(-1)
        self.callcount = 0 #used for tracking current frames and calculating values with animation curves
        AnimationInstance._instances.append(self) #Adds self to the list of all created AnimationController objects

    def _callback_wrapper(self, controller):
        '''a wrapper method for a default timer callback method. this is needed because the in-built callback method does
           not take any other arguments other than the timer that initiated the callback, and the controller where callback originated
           also needs to be tracked'''
        def _callback(timer):
            '''this is called every time a timer triggers a next 'tick' '''
            #global last_animation_flag #shared flag update-to-be i guess

            if self.callcount <= self.total_frames: #progress onto the next frame
                self.peripheral.set(self._render_frame(self.callcount))
                self.callcount += 1

            else: #finish animation instance, move on the next one if queued
                self.callcount = 0
                timer.deinit()
                if controller:
                    controller._move_to_next_step()
        return _callback

    def play(self, called_by_controller=None):
        '''ARGS >
        
        called_by_controller (None by default), used for when the animation instance is a part of an animation sequence in a controller'''
        self.callcount = 0
        self.timer.init(
            mode=machine.Timer.PERIODIC,
            period=self.ms_between_frames,
            callback=self._callback_wrapper(called_by_controller)
        )

    def kill(self):
        self.timer.deinit()

    def _render_frame(self, at_frame):
        # Normalize progression to 0.0 - 1.0
        t = at_frame / self.total_frames

         # Apply chosen easing
        if self.curve == 'cubic_in':
            eased = t ** 3
        elif self.curve == 'cubic_out':
            eased = 1 - (1 - t) ** 3
        elif self.curve == 'quint_in':
            eased = t ** 5
        elif self.curve == 'quint_out':
            eased = 1 - (1 - t) ** 5
        elif self.curve == 'quint_in_out':
            if t < 0.5:
                eased = 16 * t ** 5
            else:
                eased = 1 - ((-2 * t + 2) ** 5) / 2
        elif self.curve == 'linear':
            eased = t
        elif self.curve == 'cubic_in_out':
            if t < 0.5:
                eased = 4 * t ** 3
            else:
                eased = 1 - ((-2 * t + 2) ** 3) / 2
        elif self.curve == 'bounce':
            if t < 1 / 2.75:
                eased = 7.5625 * t * t
            elif t < 2 / 2.75:
                t -= 1.5 / 2.75
                eased = 7.5625 * t * t + 0.75
            elif t < 2.5 / 2.75:
                t -= 2.25 / 2.75
                eased = 7.5625 * t * t + 0.9375
            else:
                t -= 2.625 / 2.75
                eased = 7.5625 * t * t + 0.984375
        else:
            eased = t  # fallback to linear
        i = 0
        # Interpolate between start and end keyframes
        if(isinstance(self.start_keyframe, list)):
            value=[0, 0, 0]
            for i in range(0,3):
                value[i] = int(self.start_keyframe[i] + (self.end_keyframe[i] - self.start_keyframe[i]) * eased)
        else:
            value = int(self.start_keyframe + (self.end_keyframe - self.start_keyframe) * eased)
        #return value to set the peripheral to
        return value


        

class AnimationController():
    _instances = [] #List of all instances created, although prevents garbage collection
    
    @classmethod
    def get_instances(cls):
        '''Returns a list of all AnimationController objects created'''
        return cls._instances

    @classmethod
    def kill_all(cls):
        for instance in cls.get_instances():
            instance.sequence[instance.current_step_index].timer.deinit()

    def __init__(self, sequence, is_looping=True):
        """ARGS > 
        
        sequence:list of Animation_Instance objects
        is_looping:boolean - set to true by default"""
        self.sequence = sequence 
        self._current_step_index = 0 #used for tracking what anim is currently on
        self.is_looping = is_looping
        self.__class__._instances.append(self) #Adds self to the list of all created AnimationController objects


    @property 
    def sequence(self):
        return self._sequence
    
    @sequence.setter
    def sequence(self, val):
        if not isinstance(val, list):
            raise TypeError('must be a list of AnimationInstance objects')
        self._sequence = val

    @property 
    def current_step_index(self): #needs to be a property here so that can trigger code in current_step_index_setter
        return self._current_step_index
    
    @current_step_index.setter
    def current_step_index(self, val):
        '''triggers every time current step index gets reassigned.

        calls play() on the AnimationInstance at the new index.
        '''
        self._current_step_index = val #uptade the index
        if val !=0:
            self.sequence[self.current_step_index].play()

    def _move_to_next_step(self):
        #gets triggered by the AnimationInstance timer callback when the instance finishes playing and the next Instance can be triggered

        if self.current_step_index < len(self.sequence) - 1:
            self.current_step_index += 1
            self.sequence[self.current_step_index].play(self)
        else:
            self.current_step_index = 0
            if self.is_looping:                
                self.sequence[self.current_step_index].play(self)

    def kill(self):
        self.sequence[self.current_step_index].timer.deinit()

    def play(self):
        self._current_step_index = 0
        self.sequence[self.current_step_index].play(self) #<AnimationInstance obj  @mem>.play()
    
    def reset(self):
        self._current_step_index = 0

