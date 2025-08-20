import machine
import os

current_animation_flag = 'none' #shared flag between two cores and boot.py
last_animation_flag = 'none'



class AnimationInstance():
    _instances = []  # Prevents garbage collection

    @classmethod
    def get_instances(cls):
        return cls._instances

    @classmethod
    def kill_all(cls):
        for instance in cls.get_instances():
            instance.timer.deinit()

    def __init__(self, peripheral, curve, length, fps, start_keyframe, end_keyframe):
        self.peripheral = peripheral
        self.curve = curve
        self.length = length
        self.fps = fps
        self.total_frames = self.length * self.fps
        self.ms_between_frames = int(1000 / self.fps)
        self.start_keyframe = start_keyframe
        self.end_keyframe = end_keyframe
        self.timer = machine.Timer(-1)
        self.callcount = 0
        AnimationInstance._instances.append(self)

    def _callback_wrapper(self, controller):
        def _callback(timer):
            global last_animation_flag
            if self.callcount <= self.total_frames:
                self.peripheral.set(int(self.render_frame(self.callcount)))
                self.callcount += 1
            else:
                self.callcount = 0
                timer.deinit()
                if controller:
                    controller.move_to_next_step()
        return _callback

    def play(self, called_by_controller=None):
        self.callcount = 0
        self.timer.init(
            mode=machine.Timer.PERIODIC,
            period=self.ms_between_frames,
            callback=self._callback_wrapper(called_by_controller)
        )

    def kill(self):
        self.timer.deinit()

    def render_frame(self, at_frame):
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

        # Interpolate between start and end keyframes
        value = self.start_keyframe + (self.end_keyframe - self.start_keyframe) * eased
        return value


        

class AnimationController():
    _instances = []#prevents garbage collection but i think thats okay
    
    @classmethod
    def get_instances(cls):
        return cls._instances

    @classmethod
    def kill_all(cls):
        for instance in cls.get_instances():
            instance.sequence[instance.current_step_index].timer.deinit()

    def __init__(self, sequence, is_looping=True):
        self.sequence = sequence
        self._current_step_index = 0
        self.is_looping = is_looping
        self.__class__._instances.append(self)



    @property
    def sequence(self):
        return self._sequence
    
    @sequence.setter
    def sequence(self, val):
        if not isinstance(val, list):
            raise TypeError('must be a list of AnimationInstance objects')
        self._sequence = val

    @property
    def current_step_index(self):
        return self._current_step_index
    
    @current_step_index.setter
    def current_step_index(self, val):
        #every time current step index get reassigned this will trigger (i think)
        self._current_step_index = val
        #will autoplay the step
        if val !=0:
            self.sequence[self.current_step_index].play()

    def move_to_next_step(self):

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
        self.sequence[self.current_step_index].play(self)
    
    def reset(self):
        self._current_step_index = 0
