########################################################################################################################
#
########################################################################################################################
import boto3
from boto3.session import Session
from boto3.dynamodb.table import TableResource

from pprint import pprint


STREAM_VIEW_TYPE = "NEW_AND_OLD_IMAGES"

########################################################################################################################
#
########################################################################################################################
class aws_link():

    ####################################################################################################################
    #
    ####################################################################################################################
    def __init__(self):
        self.dynamodb:Session.resource = boto3.resource(
            'dynamodb',
            region_name="us-east-2",
            aws_access_key_id="AKIAJGM5GXVKQLGQRUOQ",
            aws_secret_access_key="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"
        )
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
            print("Got Correct Spot")
        except Exception as e:
            print(e)
        else:
            return response['Item']

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


########################################################################################################################
#
########################################################################################################################
if __name__ == '__main__':

    aws = aws_link()

    response_info = aws.get_spot("Home", 1,)
    if response_info:
        print("Get Spot succeeded:")
        pprint(response_info)

    response_info = aws.put_spot("Home", 3, 'false')
    if response_info:
        print("Put Spot succeeded:")
        pprint(response_info)