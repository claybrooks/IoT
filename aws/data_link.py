import boto3
from pprint import pprint

def get_spot(table, Location, Space, dynamodb=None):

    try:
        response = table.get_item(Key={'Location': Location, 'Spot': Space})
        print("Got Correct Spot")
    except Exception as e:
        print(e)
    else:
        return response['Item']

def put_spot(table, Location, Space, Occupied, dynamodb=None):   

    response = table.put_item(
       Item={
            'Location': Location,
            'Spot': Space,
            'Occupied': Occupied
        }
    )

    return response

if __name__ == '__main__':

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Smart_Park')

    request_info = get_spot(table, "Home", 1,)
    if request_info:
        print("Get Spot succeeded:")
        pprint(request_info)

    request_info = put_spot(table, "Home", 2, 'false')
    if request_info:
        print("Put Spot succeeded:")
        pprint(request_info)

    

    