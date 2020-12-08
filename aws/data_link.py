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

        # check the stream specification and enable it if it's disabled
        stream_spec = self.table.stream_specification
        if stream_spec is None or not stream_spec["StreamEnabled"] or stream_spec["StreamViewType"] != STREAM_VIEW_TYPE:
            self.table.update(
                StreamSpecification={
                    'StreamEnabled': True,
                    'StreamViewType': STREAM_VIEW_TYPE
                }
            )

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

    # response_info = aws.get_spot("Home", 1,)
    # if response_info:
    #     print("Get Spot succeeded:")
    #     pprint(response_info)

    # response_info = aws.put_spot("Home", 3, 'false')
    # if response_info:
    #     print("Put Spot succeeded:")
    #     pprint(response_info)

    # response_info = aws.put_spot("test", 0, True)
    # response_info = aws.update_spot("test", 0, True)
    # time.sleep(10.0)
    # response_info = aws.update_spot("test", 0, False)

    if not aws.get_spot("Smart_Park", 1):
        response_info = aws.put_spot("Smart_Park", 1, True)
    else:
        response_info = aws.update_spot("Smart_Park", 1, True)
    response_info = aws.get_spot("Smart_Park", 1)


    response_info = aws.update_spot("Smart_Park", 1, False)
    response_info = aws.get_spot("Smart_Park", 1)


    pass