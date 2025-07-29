try:
    import src.reyax as reyax
except:
    print("!couldnt import reyax.py from src!")
try:
    import src.utils as utils
except:
    print("!couldnt import utils.py from src; trying ot import from ./!")
    import utils #type:ignore
import _thread
import uasyncio #type:ignore



lock = _thread.allocate_lock()    
host_id = 65535
self_id = 2 #placeholder
led_builtin = machine.Pin(25, machine.Pin.OUT)
utils.current_animation = 'off' #shared flag between all threads and utils.py


def test_all():
    rylr.send(host_id, "testing motors!".encode("ascii"))
    print("testing motors!")
    utils.servo_test()
    rylr.send(host_id, "testing jewel!".encode("ascii"))
    print("testing jewel!")
    utils.jewel_test()
    rylr.send(host_id, "done!".encode("ascii"))
    print("done!")
    rylr.send(host_id, "setting servo to 0".encode("ascii"))
    print("setting servo to 0")
    utils.servo_set_angle(0)   



async def listen_to_host(): 
    while 1:
        received_msg = rylr.receive()
        if not received_msg == None:
            print(received_msg)
            data_parsed = received_msg.data.decode("ascii").split()
            #check received via imitating match-case; micropython does not have it :(

            #if not an animation command, handle command
            if data_parsed[0] == 'setallleds': #args > int:R, int:G, int:B
                utils.jewel_set_all(int(data_parsed[1]), int(data_parsed[2]), int(data_parsed[3]))

            elif data_parsed[0] == 'pyexec':
                #TODO: make node execute whatever python follows [remote debugging]
                pass

            #if an anitmaiton command, change the current_animation flag to let the second core handle it
            elif data_parsed[0] == 'presetoff':
                print('got off')
                lock.acquire()
                utils.current_animation = 'off'
                lock.release()     
            
            elif data_parsed[0] == 'presettest':
                print('got test')
                lock.acquire()
                utils.current_animation = 'test'
                lock.release()
            
            elif data_parsed[0] == 'presetspotlight':
                print('got spotlight')
                lock.acquire()
                utils.current_animation = 'spotlight'
                lock.release()     
            
            elif data_parsed[0] == 'presetnature':
                print('got nature')
                lock.acquire()
                utils.current_animation = 'nature'
                lock.release()
                
            elif data_parsed[0] == 'presetdystopia':
                print('got dystopia')
                lock.acquire()
                utils.current_animation = 'dystopia'
                lock.release()
                
            elif data_parsed[0] == 'presetirl':
                print('got irl')
                lock.acquire()
                utils.current_animation = 'irl'
                lock.release()
                 
    await uasyncio.sleep(0.2)


def handle_animations(): #this is the second core functionality
    lock.acquire()
    cur_anim = utils.current_animation
    lock.release()

    if cur_anim == 'off':
        utils.jewel_set_all(0, 0, 0)
        utils.servo_rotate(40)

    elif cur_anim  == 'test':
        utils.render_test_animation()

    elif cur_anim  == 'spotlight':
       utils.render_test_animation()

    elif cur_anim  == 'nature':
       utils.render_nature_animation()

    elif cur_anim  == 'irl':
       utils.render_irl_animation()

    elif cur_anim  == 'dystopia':
       utils.render_dystopia_animation()

    


print('> Setting up LoRa')
rylr = utils.connection_setup(self_id)

print("> Setting up the file system")
utils.file_system_setup()


print("> Starting server listening")
current_loop = uasyncio.get_event_loop()    # get or create the event loop
current_loop.create_task(listen_to_host())  # schedule the coroutine
current_loop.run_forever()                  # start the loop (won't return unless stopped)


print('> Starting the second thread (animation handling)')#only two per pico are possible
_thread.start_new_thread(handle_animations, ())#empty tuple is args
