from pins import *
from sensors import Sensors
from time import sleep

#sensors = Sensors([pins.tof_fleft,pins.tof_fright], ["fleft","fright"], [0x32,0x33])
# TODO:
# change BCM number according to the RPI board you are using
# method: Sensors(pins, names, addresses)
# pin number: Raspberry Pi BCM numbering
# names: human readable string
# addresses: 
sensors = Sensors([pins.tof_front,pins.tof_rear,pins.tof_left,pins.tof_right], ["front", "rear","left","right"], [0x30,0x31,0x32,0x33])

# common error: OSError: [Errno 121] Remote I/O error
# smbus cannot connect to I2C
while True:
    sensors.print_all_values()
    print()
    sleep(1)
