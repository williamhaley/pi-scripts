#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause

import time
import math
import atexit
import subprocess
import os
from subprocess import Popen

from sense import rainbow

"""
Response to joystick presses and update the Sense Hat for a Raspberry Pi
"""

x = 0
y = 0
sense = SenseHat()
rainbow_pixels = rainbow.default_pixels()

total_pixels = len(sense.get_pixels())
dim_size = int(math.sqrt(total_pixels))
max_value = dim_size - 1

processes = []

last_press_time = 0

def on_exit():
    sense.clear()

def index(x, y):
    return y * dim_size + x

def clamp(value, min_value=0, max_value=max_value):
    return min(max_value, max(min_value, value))

def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y - 1)

def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y + 1)

def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x - 1)

def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x + 1)

def refresh():
    sense.clear()
    [r, g, b] = rainbow_pixels[index(x, y)]
    sense.set_pixel(x, y, r, g, b)

def play_audio(file_name):
    global processes
    print('playing:', file_name)
    processes.append(Popen(
        ['mpg123', file_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ))

def kill_running_processes():
    global processes
    print('kill running processes')
    for process in processes:
        process.kill()
    # Must zero out or processes will be zombies and never GCed
    processes = []

def pressed(event):
    global last_pressed_time
    global processes

    print('action:', event.action)

    if event.action == ACTION_RELEASED:
        if time.time() - last_pressed_time < 0.5:
            i = index(x, y) + 1
            file_name = '{}/{}.mp3'.format(os.getcwd(), i)
            play_audio(file_name)
        else:
            kill_running_processes()
    elif event.action == ACTION_HELD:
        print('held:')
    elif event.action == ACTION_PRESSED:
        last_pressed_time = time.time()
    else:
        print('unknown action')

atexit.register(on_exit)

sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_middle = pressed
sense.stick.direction_any = refresh
refresh()
pause()
