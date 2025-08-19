import os
import machine

current_animation_flag = 'none' #shared flag between two cores and boot.py
last_animation_flag = 'none'



class AnimationInstance():
    _instances = []#prevents garbage collection but i think thats okay
    
    @classmethod
    def get_instances(cls):
        return cls._instances

    @classmethod
    def cease_all(cls):
        for instance in cls.get_instances():
            instance.timer.deinit()
            
        

    def __init__(self, peripheral, curve, length, fps, end_keyframe):#length in seconds and refresh rate in ms
        self.peripheral = peripheral
        self.curve = curve
        self.length = length
        self.fps = fps
        self.total_frames = self.length*self.fps
        self.ms_between_frames = int(1000/(self.fps))
        self.end_keyframe = end_keyframe
        self.timer = machine.Timer(-1)
        self.callcount = 0
        AnimationInstance._instances.append(self)
        
    
    def _callback(self, timer):
        global last_animation_flag
        if self.callcount <= self.total_frames:
            self.peripheral.set(int(self.render_frame(self.callcount)))
            self.callcount += 1
        else: 
            last_animation_flag = 'none'
            self.callcount = 0
            timer.deinit()


    def play(self):
        self.timer.init(mode = machine.Timer.PERIODIC, period = self.ms_between_frames, callback = self._callback)

    def render_frame(self, at_frame):
        # Normalize progression to 0.0 - 1.0
        t = at_frame/ self.total_frames

        # Apply chosen easing
        if self.curve == 'cubic_in':
            eased = t ** 3
        elif self.curve == 'cubic_out':
            eased = 1 - (1 - t) ** 3
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

        return eased * self.end_keyframe
        

class AnimationController():
    pass





























#TODO: RELOCATE THE BELOW



def file_system_setup(isverbose=False):
    filestofind = ['boot.py', 'reyax.py', 'utils.py', 'jewelutils.py', 'servoutils.py']
    for name in filestofind:
        if name not in os.listdir() and isverbose:
            print("!WARNING! "+name+" was not found in ./ directory")
    if 'src' not in os.listdir():
        os.mkdir('src')
    for name in filestofind:
        if not name == 'boot.py':
            try: 
                os.rename(name, 'src/'+name)
            except:
                if isverbose:
                    print(f'!WARNING! {name} has not been relocated')


def file_system_show():
    __traverse('', 1)


def __traverse(path, indent):
    for item in os.listdir(path):
        fullpath = path+'/'+item
        if not item.endswith('.py'):
            print('  '*indent + fullpath)
            __traverse(fullpath, indent+1)
        elif item.endswith('.py'):
            print('  '*indent + fullpath)


