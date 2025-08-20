import os
import machine


def file_system_setup(isverbose=False):
    filestofind = ['boot.py', 'reyax.py', 'utils.py', 'jewelutils.py', 'servoutils.py', 'animationutils.py', 'animations.py']
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



