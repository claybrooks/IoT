########################################################################################################################
#
########################################################################################################################
import boto3
from boto3.session import Session
from boto3.dynamodb.table import TableResource

from pprint import pprint
import time

STREAM_VIEW_TYPE = "NEW_AND_OLD_IMAGES"

########################################################################################################################
#
########################################################################################################################
class aws_link():

    ####################################################################################################################
    #
    ####################################################################################################################
    def __init__(self):
        self.dynamodb:Session.resource = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Smart_Park')

    ####################################################################################################################
    #
    ####################################################################################################################
    def get_spot(self, Location, Space):
        try:
            response = self.table.get_item(Key={'Location': Location, 'Spot': Space})
            #print("Got Correct Spot")
        except Exception as e:
            print(e)
        else:
            return response

    ####################################################################################################################
    #
    ####################################################################################################################
    def put_spot(self, Location, Space, Occupied):
        try:
            response = self.table.put_item(
            Item={
                    'Location': Location,
                    'Spot': Space,
                    'Occupied': Occupied
                }
            )
        except Exception as e:
            print(e)
        else:
            return response

    ####################################################################################################################
    #
    ####################################################################################################################
    def update_spot(self, Location, Space, Occupied):
        try:
            response = self.table.update_item(
            Key={
                'Location': Location,
                'Spot': Space
            },
            UpdateExpression="set Occupied=:o",
            ExpressionAttributeValues={
                ':o': Occupied,
            },
            ReturnValues="UPDATED_NEW"
        )
        except Exception as e:
            print(e)
        else:
            return response

    ####################################################################################################################
    #
    ####################################################################################################################
    def set_spot(self, Location, Space, Occupied):
        print (f'{Location}:{Space}={Occupied}')
        if not self.get_spot(Location, Space):
           return self.put_spot(Location, Space, Occupied)
        else:
            return self.update_spot(Location, Space, Occupied)

########################################################################################################################
#
########################################################################################################################
if __name__ == '__main__':

    aws = aws_link()

    if not aws.get_spot("Smart_Park", 1):
        response_info = aws.put_spot("Smart_Park", 1, True)
    else:
        response_info = aws.update_spot("Smart_Park", 1, True)
    response_info = aws.get_spot("Smart_Park", 1)

    time.sleep(10.0)

    response_info = aws.update_spot("location_a", 1, False)
    response_info = aws.get_spot("location_a", 1)

    # import time
    # counter = 60
    # while counter > 0:
    #     counter -= 1
    #     occupied = aws.get_spot('location_a', 1)['Item']['Occupied']
    #     print (f'{counter}: {occupied}')
    #     time.sleep(1)

    pass