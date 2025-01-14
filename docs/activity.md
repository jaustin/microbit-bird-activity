# It's alive

Let's bring our bird alive with code!

<p align="center">
<img src="/microbit-bird-activity/img/its-alive.gif" alt="It's alive gif">
</p>


## What is all this about?

<img width="30%" alt="microbit-universal-hex logo" src="/microbit-bird-activity/img/bird-with-microbit.jpg" align="right">

Your task is to think like a bird and programme the micro:bit to react to the world like a bird.

The micro:bit can communicate wirelessly with other micro:bits using radio.
There will be a secret micro:bit in the room broadcasting radio messages to
all the birds indicating different events like "saying hello" o "there is a cat
around".

Apart from that, the micro:bit contains other sensors that your bird will react
to, for example, birds don't like to be shaken!

To programme the micro:bit with Python we use 
[MicroPython (click here for more info)](https://microbit-carlos.github.io/microbit-bird-activity/micropython/)
and brand new
[Python Editor (click here for more info)](https://microbit-carlos.github.io/microbit-bird-activity/editor/).


## First steps - Load the starter project into the editor

Okay, so the first step is to open this link to the Python Editor.
This link contains a flag to enable additional beta features:
<a href="https://python.microbit.org/v/beta?flag=audioSoundEffect" target="_blank">https://python.microbit.org/v/beta?flag=audioSoundEffect</a>

To start the activity we first need to load a project hex file into the editor.

Right click on this link and select "Save Link As" to save the hex file to your
laptop: [https://github.com/microbit-carlos/microbit-bird-activity/raw/main/src/bird/bin/flockbird.hex](https://github.com/microbit-carlos/microbit-bird-activity/raw/main/src/bird/bin/flockbird.hex)

And then drag and drop the hex file to the Python Editor. The editor might
warn you that this action will replace the project, you can click "Replace" to
accept it.

### So... What am I looking at?

The loaded hex file contains two Python files, to see them let's go to "Project"
section on the left sidebar:

![Python Editor Projects](img/editor-project.png)

In this view you can switch between the `main.py` file and the `bird.py`.

- The `bird.py` module contains some functionality for the bird to be able to
react to the world.
- The `main.py` file is the main code we will be working on.

There are some comments in both files that should help clarify what things
are doing, but you can continue with the activity as we look at different
parts in steps.

The sidebar also have other useful sections:
- Reference: A place to explore the features of your micro:bit with Python
- API: The micro:bit MicroPython API developer documentation

<img width="45%" alt="microbit-universal-hex logo" src="/microbit-bird-activity/img/editor-reference.png">
<img width="45%" alt="microbit-universal-hex logo" src="/microbit-bird-activity/img/editor-api.png">


## Reacting to events

You'll see at the top of `main.py` a function called `hello()` with a decorator
`@bird.react("hello")` on top:

```python
@bird.react("hello")
def hello():
    """Somebody is saying hi, how lovely!"""
    display.show(Image.HEART)
    sleep(400)
```

When the bird detects a hello message from the airwaves, it will run this
function and show a heart image in the micro:bit display for 400 milliseconds.

<p class="exercise">
Exercise: <br>
Birds can be very chatty, so your neighbours might be saying hello quite often.
Can you think of a way to alternate between showing `Image.HEART` and
`Image.HEART_SMALL`? That way it'll look like a beating heart!
</p>

[Solution](https://github.com/microbit-carlos/microbit-bird-activity/tree/main/solutions/1-hello=beating-heart.md)

### What was that! A cat?

There are several events the bird can react to, and seeing a cat is quite important for bird survival.

<p class="exercise">
Exercise: <br>
Let's copy and paste the "hello" example, replace the function name to
`cat()`, and change the decorator argument from "hello" to "cat".
<br>
What do you think the bird should do in this case?
<br>
Some examples of thing you can do can be found in the
<a href="https://microbit-carlos.github.io/microbit-bird-activity/micropython/#quick-things-to-do-with-the-microbit" target="_blank">MicroPython page</a>.
</p>

We also want to warn other birds around us, let's do that adding by this line
at the end of the function :

```python
bird.warn_about_cat()
```

[Solution](https://github.com/microbit-carlos/microbit-bird-activity/tree/main/solutions/2-cat.md)


## Bird state

We've learned how to react to environment events (received via micro:bit
radio), what about things that happen directory to our bird?

Let's look further down `main.py` and we'll find this infinite loop.

```python
while True:
    # Look inside yourself and listen, how is your bird feeling?
    bird_state = bird.current_state()
    if bird_state == "chill":
        display.show(Image.HAPPY)
    sleep(100)
```

The function `bird.current_state()` uses the micro:bit on board sensors to
figure how your bird is doing.

<p class="exercise">
Exercise: <br>
Birds don't like to be shaken, so "angry" can also be one of the bird states
to react.
<br>
Let's expand that "if" statement with an "elif" and do something else when
the bird is "angry".
</p>

[Solution](https://github.com/microbit-carlos/microbit-bird-activity/tree/main/solutions/3-state-angry.md)


## SoundEffects

TODO: Need to explain this, and make it appeling for users to spend most of
the time here.

```python
audio.play(audio.SoundEffect(
    freq_start=400,
    freq_end=2000,
    duration=500,
    vol_start=100,
    vol_end=255,
    wave=audio.SoundEffect.WAVE_TRIANGLE,
    fx=audio.SoundEffect.FX_VIBRATO,
    interpolation=audio.SoundEffect.INTER_LOG
))
```

<p class="exercise">
Exercise: <br>
Can you come up with an "angry" sound for the bird state?
What kind of sound would a bird make if they spot a cat?
</p>

There is no "solution" for this exercise, be as creative as you'd like!
Have you tried playing multiple sounds one after another?
You can make an ever longer cooler sound 📢. 

TODO: Update this example to recreate a `micro.Sound.xxx` built in.

```python
effect_one = audio.SoundEffect(
    freq_start=400,
    freq_end=2000,
    duration=500,
    vol_start=100,
    vol_end=255,
    wave=audio.SoundEffect.WAVE_TRIANGLE,
    fx=audio.SoundEffect.FX_VIBRATO,
    interpolation=audio.SoundEffect.INTER_LOG
))

effect_two = audio.SoundEffect(
    freq_start=400,
    freq_end=2000,
    duration=500,
    vol_start=100,
    vol_end=255,
    wave=audio.SoundEffect.WAVE_TRIANGLE,
    fx=audio.SoundEffect.FX_VIBRATO,
    interpolation=audio.SoundEffect.INTER_LOG
))

effect_three = audio.SoundEffect(
    freq_start=400,
    freq_end=2000,
    duration=500,
    vol_start=100,
    vol_end=255,
    wave=audio.SoundEffect.WAVE_TRIANGLE,
    fx=audio.SoundEffect.FX_VIBRATO,
    interpolation=audio.SoundEffect.INTER_LOG
))

audio.play(effect_one, wait=False)
audio.play(effect_two, wait=False)
audio.play(effect_three, wait=False)
```

## TODO

Things that will be included here:
- [ ] Quick overview of the micro:bit
- [ ] Explain there are also a new Sound Effect system and provide example
- [ ] Make it more playful
- [ ] Proofread it
- [ ] What else?
