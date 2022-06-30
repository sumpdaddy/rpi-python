# Sump monitoring measurement call. Meant to run once per measurement.

import time
import board
import busio
import adafruit_vl53l0x

# Set up some functional details


pitbottom=600   # the approximate bottom of the pit (in mm)
meas_file="/etc/sumpdaddy"

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# set timing budget to 300ms (we are not in a hurry)
vl53.measurement_timing_budget = 300000

# Main loop will read the range in continuous mode, 1/sec
# after 40 samples it will average all samples and save result to file

with vl53.continuous_mode():

    readingsum = 0
    #  initialize the last good reading at 100mm
    oldreading = 100
    newreading = 100

    # loop for 40 seconds
    for x in range(1,40):
        # take the reading and subtract it from the bottom to get the height
        newreading = round(pitbottom-vl53.range,2)
        # check the reading is realistic, if not then keep last good reading
        if newreading < 25 or newreading > 425:
            newreading = oldreading
        # generate the average
        readingsum = readingsum + newreading
        oldreading = newreading
        time.sleep(1)

    # calculate the reading and save it to the file
    movingavg = str(readingsum/40)
    f = open(meas_file, "w")
    f.write(movingavg)
    f.close()

# stop the reading since we are about to close
vl53.stop_continuous()
