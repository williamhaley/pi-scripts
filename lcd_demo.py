#!/usr/bin/env python2

import Adafruit_CharLCD as LCD

from charlcd.menu import LCDMenu

import time
import atexit

def do_something():
    print('particular button pressed')

# Back/prev menu entries will be automatically be created for sub-menus.
menu_map = [
    { 'text': 'Menu 1', 'color': (1.0, 1.0, 0.0), 'menu': [
        { 'text': 'Something 1' },
        { 'text': 'Something 2' },
    ] },
    { 'text': 'Menu 2', 'color': (1.0, 0.0, 0.0), 'menu': [
        { 'text': 'Something 1' },
        { 'text': 'Something 2' },
    ] },
    { 'text': 'Menu 3', 'color': (0.0, 1.0, 0.0), 'action': do_something }
]

lcd = LCD.Adafruit_CharLCDPlate()

menu = LCDMenu(lcd, menu_map)

last_press = time.time()
button_timeout = 0.3
backlight_timeout = 5

def on_exit():
    lcd.clear()
    lcd.set_backlight(0)
atexit.register(on_exit)

while True:
    if time.time() - last_press > backlight_timeout:
        lcd.set_backlight(0)

    # Loop through each button type and check if it is pressed.
    for button_id in [LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT]:
        if not lcd.is_pressed(button_id):
            continue
        if time.time() - last_press < button_timeout:
            continue

        last_press = time.time()

        if button_id == LCD.LEFT:
            menu.left()
        elif button_id == LCD.RIGHT:
            menu.right()
        elif button_id == LCD.SELECT:
            menu.select()
