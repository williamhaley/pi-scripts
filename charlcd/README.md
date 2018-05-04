It is **best to follow the [official Adafruit instructions](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/usage)**, but I am consolidating the steps I needed here for my own sake. This guide is entirely based on the [example code](https://github.com/adafruit/Adafruit_Python_CharLCD/tree/master/examples) and the guides from Adafruit.

Follow their assembly guide as needed. I am still new to soldering and needed to take several attempts at re-soldering certain joints before it worked. Initially, I was getting nothing from the backlight and no characters to display until I tried again and again. I'm still working on those skills!

Once the device is properly soldered and assembled, we can use the LCD display.

Install required packages.

```
sudo apt-get install \
    build-essential \
    python-dev \
    python-smbus \
    python-pip \
    python-rpi.gpio \
    git \
    i2c-tools
```

Edit `/etc/modules` to enable the `i2c` modules we need for the LCD.

```
# /etc/modules
i2c-bcm2708
i2c-dev
```

Edit `/boot/config.txt` to enable required device overlays for the Raspberry Pi.

```
# /boot/config.txt
dtparam=i2c1=on
dtparam=i2c_arm=on
```

Reboot to enable those modules.

```
sudo reboot
```

You should see the device detected on the `i2c` bus with the following command. Adafruit has some [guides on i2c](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).

```
sudo i2cdetect -y 1
```

The LCD display should show up at address `0x20` as long as it is connected and working properly.

Clone the Adafruit LCD library.

```
git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
```

Enter that Adafruit git repo and install the library on the Raspberry Pi.

```
cd Adafruit_Python_CharLCD && \
    sudo python setup.py install
```

Adafruit has a number of [example scripts](https://github.com/adafruit/Adafruit_Python_CharLCD/tree/master/examples) that can be run to run the LCD.
