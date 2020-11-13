########################################################################################################################
# PYTHON
########################################################################################################################
import json
import os
import sys
import time


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.relpath(__file__)), '..'))
print ("Found root: " + ROOT_DIR)
sys.path.append(ROOT_DIR)


########################################################################################################################
# ZIGBEE
########################################################################################################################
from digi.xbee.devices import RemoteXBeeDevice, ZigBeeDevice
from digi.xbee.io import IOLine, IOSample, IOValue


########################################################################################################################
# AWS
########################################################################################################################
from aws.data_link import aws_link


# parameters for local zigbee serial connection
PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600


# map to enforce AWS update on change only.  The zigbees are configured to only send data on change, this is the last
# line of defense
ZIGBEE_DIO1_DATA = {}


# config that maps zigbee mac addresses to space locations
SPACE_CONFIGURATION = {}


# AWS api
AWS = aws_link()


########################################################################################################################
#
########################################################################################################################
def on_io_sample_received(sample:IOSample, remote:RemoteXBeeDevice, time:int):

    # we are only checking DIO1
    if not sample.has_digital_value(IOLine.DIO1_AD1):
        print ("Received IO sample doesn't have dio1, which is what we care about")
        return

    addr = str(remote.get_64bit_addr())
    value = sample.get_digital_value(IOLine.DIO1_AD1)

    if addr not in ZIGBEE_DIO1_DATA:
        ZIGBEE_DIO1_DATA[addr] = None

    if ZIGBEE_DIO1_DATA[addr] != value:
        print (f"New data received from {addr} => {value}")
        ZIGBEE_DIO1_DATA[addr] = value

    spaces = SPACE_CONFIGURATION['spaces']
    location = SPACE_CONFIGURATION['location']
    occupied = value == IOValue.HIGH
    if addr not in spaces:
        print (f"Address {addr} is not configured!")
    else:
        space = spaces[addr]
        print (f"Updating spot {space} in {location} to {'occupied' if occupied else 'unoccupied'}")
        AWS.put_spot(location, space, occupied)

########################################################################################################################
#
########################################################################################################################
def main():
    global SPACE_CONFIGURATION

    # create and open a serial connection to the device
    device = ZigBeeDevice(PORT, BAUD_RATE)
    device.open()

    # add a callback for the io sample
    device.add_io_sample_received_callback(on_io_sample_received)

    # read  in our space configuration
    with open(os.path.join(ROOT_DIR, 'config', 'garage_a.json')) as f:
        SPACE_CONFIGURATION = json.load(f)

    try:
        device.flush_queues()
        print("Waiting for data...\n")

        while True:
            time.sleep(1)

    finally:
        if device is not None and device.is_open():
            device.close()


########################################################################################################################
#
########################################################################################################################
if __name__ == '__main__':
    main()
