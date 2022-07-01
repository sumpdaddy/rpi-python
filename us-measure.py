#Libraries
import RPi.GPIO as GPIO
import time
import array as arr
from datetime import datetime
from decimal import Decimal

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# set up some details

runtime=50   # how many samples to get (approx seconds to run)
pitbottom=60 # approximate bottom of pit in cm
meas_file="/etc/sumpdaddy"

def distance():

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    # using an IEE754 float as a time DOES impact results since the data we need
    # is in the microsecond range, SO
    # each reading is forced to a decimal data type to preserve precision
    # everything to the left of the decimal is thrown away to preserve precision
    TimeElapsed = (Decimal(str(StopTime)) % 1) - (Decimal(str(StartTime)) % 1)


    # if the reading spanned more than 1 second, calc will be negative. so, fix that
    if TimeElapsed < 0:
        TimeElapsed = TimeElapsed + 1


    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':

    readingsum = 0


    for x in range(1,runtime):
        readingsum = readingsum + round(pitbottom-distance(),2)
        time.sleep(.95)
    movingavg = str(readingsum/runtime)
    f = open(meas_file, "w")
    f.write(movingavg)
    f.close()
    GPIO.cleanup()


