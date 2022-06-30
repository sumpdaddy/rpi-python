# SPDX-FileCopyrightText: 2021 Smankusors for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VL53L0X distance sensor with continuous mode.
# Will print the sensed range/distance as fast as possible.
import time

import board
import busio

import adafruit_vl53l0x

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
vl53.measurement_timing_budget = 300000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# You will see the benefit of continous mode if you set the measurement timing
# budget very high, while your program doing something else. When your program done
# with something else, and the sensor already calculated the distance, the result
# will return instantly, instead of waiting the sensor measuring first.

# Main loop will read the range and print it every second.

with vl53.continuous_mode():
    readingsum = 0
    oldreading = 100
    newreading = 100
    for x in range(1,40):
        newreading = round(500-vl53.range,2)
        if newreading < 25 or newreading > 325:
            newreading = oldreading
        readingsum = readingsum + newreading
        oldreading = newreading
        time.sleep(1)
    movingavg = str(readingsum/40)
    f = open("/etc/sumpdaddy", "w")
    f.write(movingavg)
    f.close()
vl53.stop_continuous()
