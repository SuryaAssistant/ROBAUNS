#GPIO for the IR receiver: 23
#GPIO for the IR transmitter: 14
import time
import os

os.system ("sudo pigpiod")
from ircodec.command import CommandSet

controller = CommandSet.load('Ardoor.json')
time.sleep (1)
controller.emit('Trigger')
print ('Sinyal terkirim')