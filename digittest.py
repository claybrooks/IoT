from digi.xbee.devices import XBeeDevice
import digi
import sys

device = XBeeDevice("COM6", 9600)
device.open()

exit = False

while not exit:
    next = input('Enter Message: ')
    if next == 'exit':
        exit = True
    try:
        device.send_data_broadcast(next)
    except digi.xbee.exception.TimeoutException:
        print ("Failed to send")

device.close()