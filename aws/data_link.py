import boto3
from pprint import pprint

class aws_link():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Smart_Park')

    def get_spot(self, Location, Space):
        try:
            response = self.table.get_item(Key={'Location': Location, 'Spot': Space})
            print("Got Correct Spot")
        except Exception as e:
            print(e)
        else:
            return response['Item']

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

if __name__ == '__main__':

    aws = aws_link()

    response_info = aws.get_spot("Home", 1,)
    if response_info:
        print("Get Spot succeeded:")
        pprint(response_info)

    response_info = aws.put_spot("Home", 3, 'true')
    if response_info:
        print("Put Spot succeeded:")
        pprint(response_info)