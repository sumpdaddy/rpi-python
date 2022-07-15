# rpi-python
Sump monitoring tools for Rpi

tof-measure.py is a script meant to be used with VL53L0X sensor attached to I2C bus 1, started once per measurement

us-measure.py is a script meant to be used with a HC-SR04 attached to GPIO18/24, started once per measurement 

These work nicely via crontab either every minute, every 5 minutes, etc based on how badass you want your monitoring to be.  They will save to a file in /etc and then Cacti can pick up that reading and create a graph

Basic How-To

1.  Provision a Raspberry Pi using a debian-based OS (raspberry pi os, any recent version)  
    1a.  Install cacti 'apt install cacti'  
    1b.  Confirm python is ready 'apt install python3 python3-pip'  
2.  Attach your HC-SR04 sensor to GPIO 18 and 24 (plenty of good generic howtos exist)  
    2a. No special libraries are required  
3.  AND/OR attach your VL53L0X sensor to I2C bus (plenty of good generic howtos exist)   
    3a. Install the adafruit I2C bus library 'pip3 install adafruit-circuitpython-busdevice'  
    3b. Install the adafruit VL53L0X library 'pip3 install adafruit-circuitpython-vl53l0x'  
4.  Copy the python scripts (contin and measure) for the device you want to use to your system (works fine in the user home or other dir)  
5.  Run the contin script to verify your readings are valid.  
    5a. the scripts assume the sensor is going to be about 60cm from the bottom of the pit (adjust the value in the measure script as needed)  
6.  Install your device to your sump with the sensor pointing away from your face.  
7.  Add the measure script to your cacti cron: 'sudo nano /etc/cron.d/cacti'  
    7a. I like to also bump cacti to 1 min intervals here instead of 5min (just change cacti poller line to all stars)  
    7b. Crontab should look something like the attached file (Based on your home folder where you put the script)  
8.  Add the cacti template to your system  
    8a. it is set up to assume your file goes to /etc/sumpdaddy, if you changed this in the python then also change it in the data input method for 'Sump Distacnce'  
    8b. if you want metric units instead of freedom units simply edit the CDEF under Presets called 'mm to inch' and you can do 'mm to cm' or 'mm to mm' for all I care  
9.  Create a monitored device for your local system (plenty of good generic howtos exist)  
10. Add the Sump Level graph to the device to start monitoring  
11. Enjoy your nifty new sump graph  
