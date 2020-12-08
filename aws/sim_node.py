########################################################################################################################
#
########################################################################################################################
from data_link import aws_link
import time
import argparse

aws = aws_link()

location = "location_b"
spot = 1
time_s = 10

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--location', help="Garage Location of Node")
parser.add_argument('-s', '--spot', help="Spot of Vehicle", type=int)
parser.add_argument('-t', '--time', help="Time in Spot (in seconds)", type=int)

args = parser.parse_args()

if args.location:
    location=args.location 

if args.spot:
    spot=args.spot 

if args.time:
    time_s = args.time

    if not aws.get_spot(location, int(spot)):
        response_info = aws.put_spot(location, int(spot), True)
    else:
        response_info = aws.update_spot(location, int(spot), True)

    time.sleep(int(time_s))

    response_info = aws.update_spot(location, int(spot), False)

