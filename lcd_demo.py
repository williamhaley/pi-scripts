#!/usr/bin/env python2

import Adafruit_CharLCD as LCD

from charlcd.menu import LCDMenu
import alsaaudio

import time
import atexit
import os
from time import sleep
import socket
import subprocess
from subprocess import Popen
from subprocess import signal

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# For now, only handle audio files.
def file_handler(path):
	global last_process
	kill_last_file_handler()
	with open(os.devnull, 'w') as FNULL:
		try:
			last_process = Popen(['mpg123', path], stdout=FNULL, stderr=FNULL)
		except subprocess.CalledProcessError:
			print("error running mpg123 with " + path)

def kill_last_file_handler():
    global last_process
    if last_process is None:
        return
    # Only kill if the process is still running. None indicates running.
    if last_process.poll() is None:
        # Send SIGINT. kill() seems to screw up the tty.
        last_process.send_signal(signal.SIGINT)
        last_process.wait()

def power_off():
	global lcd
	lcd.clear()
	lcd.set_backlight(0.0)
	os.system("shutdown now -h")

def show_ip():
	global lcd
	lcd.clear()
	lcd.message('IP:\n' + get_ip())
	sleep(2)
	global lcd_menu
	lcd_menu.update_menu()

def volume_up():
	global mixer
	# Just use the first channel.
	vol = mixer.getvolume()[0]
	vol = min(vol + 10, 100)
	print("Volume set to: " + str(vol))
	mixer.setvolume(vol)

def volume_down():
	global mixer
	# Just use the first channel.
	vol = mixer.getvolume()[0]
	vol = max(vol - 10, 0)
	print("Volume set to: " + str(vol))
	mixer.setvolume(vol)

# Back/prev menu entries will be automatically be created for sub-menus.
menu_map = [
    { 'text': 'Tuba',   'color': (1.0, 1.0, 0.0), 'dir_list': '/home/pi/Music' },
    { 'text': 'Sounds', 'color': (0.0, 0.0, 1.0), 'dir_list': '/home/pi/Sounds' },
    { 'text': 'System', 'color': (1.0, 0.0, 1.0), 'menu': [
        { 'text': 'Show IP',  'action': show_ip   },
        { 'text': 'Shutdown', 'action': power_off },
    ] },
]

lcd = LCD.Adafruit_CharLCDPlate()
mixer = alsaaudio.Mixer('Master')

lcd_menu = LCDMenu(lcd, menu_map, lambda x: file_handler(x))

last_action = time.time()
backlight_timeout = 5
last_process = None
last_press = 0
dispatchable_action = None

def on_exit():
    lcd.clear()
    lcd.set_backlight(0)
    kill_last_file_handler()
atexit.register(on_exit)

left = False
right = False
up = False
down = False
select = False

while True:
    # Turn off the backlight to save power.
    if time.time() - last_action > backlight_timeout:
        lcd.set_backlight(0)

    # Loop through each button type and check if it is pressed.
    for button_id in [LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT]:
        if not lcd.is_pressed(button_id):
            continue

        # Any button is pressed. Track the time.
        last_press = time.time()

        # Track which buttons are now pressed.
        if button_id == LCD.LEFT:
            left = True
        if button_id == LCD.RIGHT:
            right = True
        if button_id == LCD.UP:
            up = True
        if button_id == LCD.DOWN:
            down = True
        if button_id == LCD.SELECT:
            select = True

    # Any button is pressed.
    if left or right or up or down or select:
        # It's been more than 0.1 seconds. Ample time for a human to have held
        # down multiple buttons if they wanted. Humans are not perfect. The odds
        # of a human hitting two buttons at the *exact* same time are very slim.
        # Having this threshold helps account for that imperfection.
        if time.time() - last_press > 0.1:
            # Any action should wake the screen back up if it was off.
            lcd_menu.wake_up()

            print('l: ' + str(left) + ' r: ' + str(right) + ' u: ' + str(up) + ' d: ' + str(down) + ' select: ' + str(select))

            if left and right:
                kill_last_file_handler()
            elif left:
                lcd_menu.left()
            elif right:
                lcd_menu.right()
            elif up:
                volume_up()
            elif down:
                volume_down()
            elif select:
                lcd_menu.select()

            last_action = time.time()

            # Reset button states so we can detect a new "press".
            left = False
            right = False
            up = False
            down = False
            select = False

