########################################################################################################################
# PYTHON
########################################################################################################################
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
from digi.xbee.io import IOLine, IOSample


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


########################################################################################################################
#
########################################################################################################################
def on_io_sample_received(sample:IOSample, remote:RemoteXBeeDevice, time:int):

    # we are only checking DIO1
    if not sample.has_digital_value(IOLine.DIO1_AD1):
        print ("Received IO sample doesn't have dio1, which is what we care about")
        return

    addr = remote.get_64bit_addr()
    value = sample.get_digital_value(IOLine.DIO1_AD1)

    if addr not in ZIGBEE_DIO1_DATA:
        ZIGBEE_DIO1_DATA[addr] = None

    if ZIGBEE_DIO1_DATA[addr] != value:
        print (f"New data received from {addr} => {value}")
        ZIGBEE_DIO1_DATA[addr] = value


########################################################################################################################
#
########################################################################################################################
def main():

    # create and open a serial connection to the device
    device = ZigBeeDevice(PORT, BAUD_RATE)
    device.open()

    # add a callback for the io sample
    device.add_io_sample_received_callback(on_io_sample_received)

    # open up our aws link
    # aws = aws_link()

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
