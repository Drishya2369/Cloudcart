"""
CloudCart — order_processor Lambda function

Phase 2: receives an order via API Gateway (HTTP API, POST /order_processor)
and persists it to the DynamoDB Orders table.

Region: eu-west-1 (must match the Orders table region)
"""

import boto3
import json


def lambda_handler(event, context):

    # Step 1: Log the incoming event for CloudWatch
    print("Received event:", json.dumps(event))

    # Step 2: Parse the order payload from the request body
    body = json.loads(event['body'])

    # Step 3: Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('Orders')

    # Step 4: Persist the order
    table.put_item(Item={
        'orderId': body['orderId'],
        'customerName': body['customerName'],
        'product': body['product'],
        'amount': body['amount'],
        'status': 'received'
    })

    # Step 5: Return a confirmation response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Order received successfully!',
            'orderId': body['orderId']
        })
    }
