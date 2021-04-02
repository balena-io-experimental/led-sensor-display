import RPi.GPIO as GPIO
import board
from adafruit_ht16k33.segments import Seg7x4
import requests
import time
import os

# This method fires on edge detection from the mode button
def on_mode(channel):
    global mode, data_len
    mode = mode + 1
    if mode > (data_len - 1):
        mode = 0
    print("Mode changed to {0}".format(mode))
    disp_mode = str(mode)
    display.print(disp_mode.rjust(2,'0') + ":  ")

# Start display mode at zero or env var
mode = int(os.getenv('DISPLAY_INDEX', '0'))

data_len = 8 # default for pulse block

# Set up display and brightness
# Display set to GPIO.BCM by adafruit library
i2c = board.I2C()
display = Seg7x4(i2c)
display.brightness = 0.5

# Quick LED test all segments at startup
display.fill(1)
time.sleep(1.2)
display.fill(0)

# Set up mode button GPIO input
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(16, GPIO.FALLING, callback=on_mode, bouncetime=250)

while True:
    try:
        r = requests.get('http://pulse:7575')
    except requests.exceptions.RequestException as e:
        # Any problem getting data, display error and keep trying...
        print("Data request error: {0}".format(str(e)))
    else:
        pulse_data = r.json()
        disp_data = list(pulse_data.values()) # Convert data dict to a list of values
        data_len = len(disp_data)
        this_data = disp_data[mode]
        if type(this_data) == str:
            # Just display the four leftmost characters if text
            disp_tmp = disp_data[mode][0:4]
            disp_out = disp_tmp.ljust(4, " ")
        else:
            # Numeric, so format as best as possible for four digit display
            if this_data > 9999.99:
                temp_disp = "e" + str(this_data / 1000)
                disp_out = temp_disp[0:5]
            elif isinstance(this_data, int):
                disp_out = str(this_data).rjust(4, "0")
            else:
                disp_out = str(this_data).ljust(4, "0")[0:5]
        time.sleep(0.5)   # minumum wait after changing the mode
        display.colon = False  # Make sure the colon is off
        display.print(disp_out)

    time.sleep(2)
