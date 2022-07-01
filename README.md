# rpi-python
Sump monitoring tools for Rpi

tof-measure.py is a script meant to be used with VL53L0X sensor attached to I2C bus 1, started once per measurement

us-measure.py is a script meant to be used with a HC-SR04 attached to GPIO18/24, started once per measurement 

These work nicely via crontab either every minute, every 5 minutes, etc based on how badass you want your monitoring to be.  They will save to a file in /etc and then Cacti can pick up that reading and create a graph
