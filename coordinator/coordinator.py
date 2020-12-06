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
NODE_DATA = {}


# config that maps zigbee mac addresses to space locations
SPACE_CONFIGURATION = {}


# map of string space names to their associated DIO lines
SPACE_TO_DIO_LINE = {
    1: IOLine.DIO1_AD1,
    2: IOLine.DIO2_AD2,
    3: IOLine.DIO3_AD3,
    4: IOLine.DIO4_AD4,
    5: IOLine.DIO5_AD5,
    6: IOLine.DIO6,
    7: IOLine.DIO7,
    8: IOLine.DIO8,
    9: IOLine.DIO9,
}


# AWS api
AWS = aws_link()


########################################################################################################################
#
########################################################################################################################
def on_io_sample_received(sample:IOSample, remote:RemoteXBeeDevice, time:int):

    # get the address of the sender node
    addr = str(remote.get_64bit_addr())

    # add this address to our node data if it doesn't exist
    if addr not in NODE_DATA:
        NODE_DATA[addr] = {}

    # Data we have about our configured nodes
    nodes       = SPACE_CONFIGURATION['nodes']

    if str(addr) not in nodes:
        print (f'addr {addr} not in configuration file!!')
        return

    # Data we have about the node that triggered this callback
    node        = nodes[str(addr)]
    # The name of this garage
    location    = SPACE_CONFIGURATION['location']

    # go through each dio and see if the incoming IOSample has it and what it's value is
    for s in node:
        config_dio = s['dio']
        space = int(s['space'])

        # unpack useful configuration data
        dio = SPACE_TO_DIO_LINE[config_dio]

        if not sample.has_digital_value(dio):
            print (f"Incoming dio line {dio} from addr {addr} is not configured!")
            continue

        # Get the current known state of this dio line
        current = NODE_DATA[addr].get(dio, None)
        # Get the new state of this dio line
        new = sample.get_digital_value(dio)

        # if they are the same, just continue
        if new == current:
            print (f"Incoming dio line {dio} from addr {addr} is the same!")
            continue

        print (f"New data received from {addr} => {str(dio)}={new}")

        # update our internal map of data
        NODE_DATA[addr][dio] = new

        # see if the space is occupied
        occupied = new == IOValue.HIGH

        # send it off to aws
        AWS.set_spot(location, space, occupied)


########################################################################################################################
#
########################################################################################################################
def main():
    global SPACE_CONFIGURATION

    # read  in our space configuration
    with open(os.path.join(ROOT_DIR, 'config', 'garage_a_v2.json')) as f:
        SPACE_CONFIGURATION = json.load(f)

    # create and open a serial connection to the device
    device = ZigBeeDevice(PORT, BAUD_RATE)
    device.open()

    try:
        device.flush_queues()
        print("Waiting for data...\n")

        # add a callback for the io sample
        device.add_io_sample_received_callback(on_io_sample_received)

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
