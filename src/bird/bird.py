# microbit-module: bird@0.0.1
# Welcome to the bird brain, processing the world around it!
# The bird notices several 'events' that can happen in their environment
# and can react to them.
# These events are processed via the @react("event_name") decorator in main.py
#     - hello: new bird has arrived in the flock
#     - cat : predator below
#     - hawk: predator above
#     - dawn: time to wake up
#     - dusk: time to go to sleep
#     - ...extend your bird by editing the bird.py file!
#
# The bird can also
#     - food: time for dinner
#     - squawk: something loud happened
#     - motion: some kind of movement happened
#     - chill: nothing is happening, rest
#
# Modules imported with __ to keep them out of the autocompletion in main.py
import radio as __radio
import microbit as __mb
import machine as __machine
import struct as __struct
import random as __rand

BIRD_NAME = None
__MSG_DELIMITER = "->"
__RADIO_GROUP_HELLO = 1
__RADIO_GROUP_BIRDS = 17

# Defined radio messages to react to
_events = ["hello", "cat", "hawk", "food", "dawn", "dusk"]
_states = ["chill", "hungry", "angry"]

# Callbacks for the react decorator


class react():
    """Decorator to register function callbacks for events (radio messages)."""

    callbacks = dict()

    def __init__(self, radio_event):
        """:param radio_event: String with the event to register."""
        if radio_event not in _events:
            raise Exception("Invalid message event string in @react decorator.")
        self.radio_event = radio_event

    def __call__(self, original_func):
        self.callbacks[self.radio_event] = original_func
        def wrappee(*args, **kwargs):
            return original_func(*args,**kwargs)
        return wrappee


def __hi_everyone_i_am_here():
    """Say hello to the world until you hear hello back to you.
    The micro:bit that transmits radio events keeps a list of active birds,
    so this is a way to register your bird is active.
    """
    print("👋 Hello, my name is {}. Can anybody hear me...?".format(BIRD_NAME))
    __radio.config(group=__RADIO_GROUP_HELLO, power=7)
    __radio.on()
    msg_out = "hello{}{}".format(__MSG_DELIMITER, BIRD_NAME)
    timeout = __mb.running_time() + (30 * 1000)
    while __mb.running_time() < timeout:
        try:
            __radio.send(msg_out)
            __mb.sleep(__rand.randint(100,300))
            radio_received = __radio.receive()
        except:
            pass
        else:
            if radio_received == msg_out:
                # So glad somebody said hello back, I can go on with my business now
                print("🎉 Somebody said hello back, this is such a friendly neighbourhood!")
                break
    else:
        # I've been waiting too long to be acknowledged
        print("Warning! Bird could not hear any hello back.")
    # Move to the radio group with all the birds
    __radio.config(group=__RADIO_GROUP_BIRDS, power=1)


def __friendly_name():
    """Returns a string with a friendly name based on MCU Unique ID."""
    length, letters = 5, 5
    codebook = [
        ['z', 'v', 'g', 'p', 't'],
        ['u', 'o', 'i', 'e', 'a'],
        ['z', 'v', 'g', 'p', 't'],
        ['u', 'o', 'i', 'e', 'a'],
        ['z', 'v', 'g', 'p', 't']
    ]
    name = []
    # Derive our name from the unique ID
    _, n = __struct.unpack("II", __machine.unique_id())
    ld = 1;
    d = letters;
    for i in range(0, length):
        h = (n % d) // ld;
        n -= h;
        d *= letters;
        ld *= letters;
        name.insert(0, codebook[i][h]);
    return "".join(name);


@__mb.run_every(s=2)
def __check_radio_msgs():
    try:
        msg = __radio.receive()
    except:
        print("Warning: There was an unexpected error reading radio.")
        return
    try:
        if msg:
            __process_world(msg)
    except Exception as e:
        print("Warning: There was an error processing the world")
        print(e)


def __process_world(message):
    # First check if this message is for us
    global BIRD_NAME
    msg_split = message.split(__MSG_DELIMITER)
    if len(msg_split) != 2:
        print("👂❗️ Heard something weird! Not quite sure what it means:".format(message))
        return
    if msg_split[1] not in [BIRD_NAME, "all"]:
        # This message is for a different bird, we can ignore it
        return

    # Okay, the message is for us, let's figure out what to do with it!
    print("👂 I've heard something: {}".format(message))
    # First we run any code specific for the message
    if msg_split[0] == "hello":
        __hi_everyone_i_am_here()
    # Then we run the user callback
    if msg_split[0] in react.callbacks:
        react.callbacks[msg_split[0]]()
    return
    # Check for radio signals:
    # for us/under the hood: 
        # stop
        # start
    # for the user:
        # hello: new bird
        # cat : predator below
        # hawk: predator above
        # food: time for dinner
        # dawn: time to wake up
        # dusk: time to go to sleep
    if message:
        if message == "stop":
            #sleep!
            #while we don't have sleep, just loop waiting for the start command
            #__wait_for_start()
            pass
        elif (message == "hawk"  or message == "cat"):
            #impose a small delay before warning others
            __mb.sleep(200)
            return message
        else:
            if message in _events:
                return message


def current_state():
    # Check for a loud noise
    if __mb.microphone.current_event() == __mb.SoundEvent.LOUD:
        return 'squawk'
    # Check for motion
    if __mb.accelerometer.was_gesture('shake'):
        return 'motion'
    __mb.sleep(10)   # Ensure run_every has a chance to run
    return "chill"


def warn_about_hawk():
    __radio.send("hawk->all")


def warn_about_cat():
    __radio.send("cat->all")


def __init():
    global BIRD_NAME
    BIRD_NAME = __friendly_name()
    __hi_everyone_i_am_here()


# We run some init code on import
__init()
