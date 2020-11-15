import json
import boto3
import datetime

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            if record['eventName'] == 'INSERT':
                handle_insert(record)
            elif record['eventName'] == 'MODIFY':
                handle_modify(record)
            elif record['eventName'] == 'REMOVE':
                handle_remove(record)
        
    except Exception as e:
        print(e)
        return "An Exception has occurred"

def handle_insert(record):
    print('Handling INSERT event')
    client = boto3.resource('dynamodb')
    table = client.Table('Smart_Park')
    print(table.table_status)
    
    print(record['dynamodb']['NewImage']['Location']['S'])
    print(record['dynamodb']['NewImage']['Spot']['N'])
    print(record['dynamodb']['NewImage']['Occupied']['BOOL'])
    
    response = table.update_item(
        Key={
            'Location':str(record['dynamodb']['NewImage']['Location']['S']),
            'Spot':int(record['dynamodb']['NewImage']['Spot']['N'])
        },
        UpdateExpression="set Occupied=:o, TimeIn=:t",
        ExpressionAttributeValues={
            ':o': record['dynamodb']['NewImage']['Occupied']['BOOL'],
            ':t': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
    
def handle_modify(record):
    print('Handling MODIFY event')
    client = boto3.resource('dynamodb')
    table = client.Table('Smart_Park')
    print(table.table_status)
    
    print(record['dynamodb']['NewImage']['Location'])
    print(record['dynamodb']['NewImage']['Spot'])
    print(record['dynamodb']['NewImage']['Occupied'])
    
    newImage = record['dynamodb']['NewImage']['Location']
    location = newImage.get('S')
    print("Location: " + str(location))
    
    newImage = record['dynamodb']['NewImage']['Spot']
    spot = newImage.get('N')
    print("Spot: " + str(spot))
    
    newImage = record['dynamodb']['NewImage']['Occupied']
    oldImage = record['dynamodb']['OldImage']['Occupied']
    occupiedNew = newImage.get('BOOL')
    occupiedOld = oldImage.get('BOOL')
    print("Occupied New: " + str(occupiedNew))
    print("Occupied Old: " + str(occupiedOld))
    
    timeIn = ''
    billedTime = ''
    
    if 'TimeIn' in record['dynamodb']['NewImage']:
        newImage = record['dynamodb']['NewImage']['TimeIn']
        print('NewImg1: ' + str(newImage))
        timeIn = newImage.get('S')
    
    if 'BilledTime' in record['dynamodb']['NewImage']:
        newImage = record['dynamodb']['NewImage']['BilledTime']
        print('NewImg2: ' + str(newImage))
        billedTime = newImage.get('S')
    
    if occupiedNew == False and occupiedOld == True:
        oldTime = datetime.datetime.strptime(timeIn,"%m/%d/%Y, %H:%M:%S")
        newTime = datetime.datetime.now()
        print("Hit1")
        billedTime = newTime - oldTime
        print("Billed Time: " + str(billedTime))
        timeIn = 'Currently Out'
    elif occupiedNew == True and occupiedOld == False:
        timeIn = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        billedTime = ''
    
    response = table.update_item(
        Key={
            'Location':str(record['dynamodb']['NewImage']['Location']['S']),
            'Spot':int(record['dynamodb']['NewImage']['Spot']['N'])
        },
        UpdateExpression="set Occupied=:o, TimeIn=:t, BilledTime=:b",
        ExpressionAttributeValues={
            ':o': record['dynamodb']['NewImage']['Occupied']['BOOL'],
            ':t': str(timeIn),
            ':b': str(billedTime)
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    
def handle_remove(record):
    print('Handling REMOVE event')