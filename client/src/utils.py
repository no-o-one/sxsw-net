import os


current_animation = 'none' #shared flag between two cores and boot.py


def file_system_setup():
    filestofind = ['boot.py', 'reyax.py', 'utils.py', 'jewelutils.py', 'servoutils.py']
    for name in filestofind:
        if name not in os.listdir():
            print("!WARNING! "+name+" was not found in ./ directory")
    if 'src' not in os.listdir():
        os.mkdir('src')
    for name in filestofind:
        if not name == 'boot.py':
            try: 
                os.rename(name, 'src/'+name)
            except:
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


#ANIMATION RENDERERS--- will also have to actively check the current_animation because threading is a  - this is terrifying please whta the fuck

#hold pause deal with it later

# def render_test_animation(speed=0.001):
#     global current_animation
#     for intensity in range(0, 256):
#         if current_animation == 'test':
#             jewel_set_all(intensity, 0, 0)
#             time.sleep(speed)
#         else:
#             break
#     for intensity in range(255, -1, -1):
#         if current_animation == 'test':
#             jewel_set_all(intensity, 0, 0)
#             time.sleep(speed) 
#         else: 
#             break

#     for intensity in range(0, 256):
#         if current_animation == 'test':
#             jewel_set_all(0, intensity, 0)
#             time.sleep(speed)
#         else:
#             break
#     for intensity in range(255, -1, -1):
#         if current_animation == 'test':
#             jewel_set_all(0, intensity, 0)
#             time.sleep(speed)  
#         else: 
#             break

#     for intensity in range(0, 256):
#         if current_animation == 'test':
#             jewel_set_all(0, 0, intensity)
#             time.sleep(speed)
#         else:
#             break
#     for intensity in range(255, -1, -1):
#         if current_animation == 'test':
#             jewel_set_all(0, 0, intensity)
#             time.sleep(speed)  
#         else:
#             break
#     current_animation = 'off'

# def render_spotlight_animation():
#     global current_animation
#     while current_animation == 'spotlight':
#         jewel_set_all(50,50,50)
#         servo_rotate(80, 0.005)

#         if not current_animation == 'spotlight':
#             break
            
#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'spotlight':
#                 break
        
#         jewel_set_all(0,0,0)
#         servo_rotate(140, 0.005)

#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'spotlight':
#                 break
    
#         jewel_set_all(100,100,100)
#         servo_rotate(80, 0.005)

#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'spotlight':
#                 break
        
#         jewel_set_all(0,0,0)
#         servo_rotate(140, 0.005)

#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'spotlight':
#                 break



# def render_dystopia_animation():
#     global current_animation
#     while current_animation == 'dystopia':
#         jewel_set_all(50,50,50)
#         servo_rotate(80, 0.005)

#         if not current_animation == 'dystopia':
#             break
            
#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'dystopia':
#                 break
        
#         jewel_set_all(150,0,0)
#         servo_rotate(140, 0.005)

#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'dystopia':
#                 break
    
#         jewel_set_all(100,100,100)
#         servo_rotate(80, 0.005)

#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'dystopia':
#                 break
        
#         jewel_set_all(100,0,0)
#         servo_rotate(140, 0.005)

#         to = time.sleep(random.randint(1, 10))
#         for wait in range(0, to, 0.2):
#             time.sleep(wait)
#             if not current_animation == 'dystopia':
#                 break


# def render_nature_animation():
#     global current_animation
#     jewel_set_all(111,158,93)
#     if not current_animation == 'nature':
#         pass
#     servo_rotate(180, 0.02)
#     if not current_animation == 'nature':
#         pass

#     jewel_set_all(111,148,113)
#     if not current_animation == 'nature':
#         pass
#     servo_rotate(140, 0.02)
#     if not current_animation == 'nature':
#         pass



# async def render_irl_animation(lock):#uasyncio.sleep(0) are sprinkled in here to make sure other functions in boot.py still run
#     global current_animation
    
#     #light up softly white
#     for i in range(0, 10):
#         jewel_set_all(i, i, i)
#         await uasyncio.sleep(0.05)

#     #open
#     servo_rotate(40)
#     await uasyncio.sleep(0)
#     servo_rotate(70, 0.008)
#     await uasyncio.sleep(0)
#     servo_rotate(110, 0.012)
#     await uasyncio.sleep(0)
#     servo_rotate(160, 0.018)
#     await uasyncio.sleep(0)
#     servo_rotate(180, 0.026)
#     await uasyncio.sleep(0)

#     #fade to purple 90, 10, 130
#     for i in range(10, 130):
#         if i < 90:
#             jewel_set_all(i, 10, i)
#         else:
#            jewel_set_all(90, 10, i) 
#         await uasyncio.sleep(0.05)
    
#     #chill
#     await uasyncio.sleep(5)

#     #close
#     servo_rotate(160, 0.026)
#     await uasyncio.sleep(0)
#     servo_rotate(110, 0.018)
#     await uasyncio.sleep(0)
#     servo_rotate(70, 0.012)
#     await uasyncio.sleep(0)
#     servo_rotate(40, 0.008)
#     await uasyncio.sleep(0)
   
#     #reset animation done, reset the tracker in a safe fashion so that the animation can re trigger if needed
#     lock.acquire()
#     current_animation = 'none'
#     lock.release()
