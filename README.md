# led-sensor-display
Display the data output of the [sensor block](https://github.com/balenablocks/sensor) or [pulse block](https://github.com/balenablocks/pulse) on a seven-segment LED display, as seen on the balena [IoT Happy Hour #47](https://youtu.be/GLzRwLen6Hc?t=2879)

![alt-text](https://github.com/balena-io-playground/led-sensor-display/blob/main/images/IMG_4873.jpg)

## Overview

This project uses an I2C four digit LED display such as [this one](https://www.adafruit.com/product/881) from Adafruit. (They are available in other colors as well!) Our example uses the Raspberry Pi 3A but any Pi should work. You can add a button to GPIO16 (pin 36) to toggle through the data fields being displayed. You can also set the device variable `DISPLAY_INDEX` to the index of the data field (starting with 0) you want as a default value displayed on startup. (This is useful if you don't add a button and don't want the first value displayed.) In our example, we also wired a button to GPIO20 to reset the counter in the pulse block.

## Usage

Connect the display to the pi as [outlined here](https://learn.adafruit.com/adafruit-led-backpack/0-dot-56-seven-segment-backpack-python-wiring-and-setup). Then include this repo in your project and add this to your existing docker-compose file:
```
  counter:
    build: ./counter
    restart: always
    privileged: true
```
(Assuming you placed these files in a folder named "counter".)

## The Display

Every time you click the display button, the two leftmost digits will temporarily display the index number of the data along with a colon. It will then display that data. It can display alphabetical characters a - f (the hex letters) but any others will show as blank. If a value exceeds the display capacity of 9999, it will switch to displaying the number in thousands. In that case, an "E" will be displayed for the first digit. For example, the value 147,616 will be displayed as "E147" and the value 12,611 would be displayed "E12.6".
