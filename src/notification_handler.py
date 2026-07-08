import boto3
import json

SNS_TOPIC_ARN = "arn:aws:sns:eu-west-1:442729101590:cloudcart-notifications"

def lambda_handler(event, context):
    sns = boto3.client('sns', region_name='eu-west-1')
    for record in event['Records']:
        order = json.loads(record['body'])
        message = (
            f"New Order Received!\n\n"
            f"Order ID   : {order['orderId']}\n"
            f"Customer   : {order['customerName']}\n"
            f"Product    : {order['product']}\n"
            f"Amount     : ₹{order['amount']}\n"
            f"Status     : Received & Processing"
        )
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"CloudCart Order Confirmation — {order['orderId']}",
            Message=message
        )
    return {'statusCode': 200}
