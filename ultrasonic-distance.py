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
    TimeElapsed = (Decimal(str(StopTime)) % 1) - (Decimal(str(StartTime)) % 1)
    if TimeElapsed < 0:
        TimeElapsed = TimeElapsed + 1


    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':

    readingsum = 0


    for x in range(1,55):
        readingsum = readingsum + round(50-distance(),2)
        time.sleep(.95)
    movingavg = str(readingsum/55)
    f = open("/etc/sumpdaddy", "w")
    f.write(movingavg)
    f.close()
    GPIO.cleanup()


