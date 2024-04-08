import json
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = 'ProductTable'  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    http_method = event['httpMethod']
    if event['resource'] == '/health':
        return {'statusCode': 200, 'body': 'Healthy'}

    if event['resource'] == '/product':
        if http_method == 'GET':
            return get_product(event)
        elif http_method == 'POST':
            return create_product(event)
        elif http_method == 'PATCH':
            return update_product(event)
        elif http_method == 'DELETE':
            return delete_product(event)

    if event['resource'] == '/products':
        if http_method == 'GET':
            return get_all_products(event)

    return {'statusCode': 404, 'body': 'Resource not found'}


def get_product(event):
    product_id = event['queryStringParameters']['id']
    response = table.get_item(Key={'product_id': product_id})
    if 'Item' in response:
        return {'statusCode': 200, 'body': json.dumps(response['Item'])}
    else:
        return {'statusCode': 404, 'body': 'Product not found'}


def create_product(event):
    data = json.loads(event['body'])
    table.put_item(Item=data)
    return {'statusCode': 201, 'body': 'Product created successfully'}


def update_product(event):
    data = json.loads(event['body'])
    product_id = data['product_id']
    response = table.update_item(
        Key={'product_id': product_id},
        UpdateExpression='SET #name = :name, #price = :price',
        ExpressionAttributeNames={'#name': 'name', '#price': 'price'},
        ExpressionAttributeValues={':name': data['name'], ':price': data['price']},
        ReturnValues='UPDATED_NEW'
    )
    return {'statusCode': 200, 'body': 'Product updated successfully'}


def delete_product(event):
    product_id = json.loads(event['body'])['product_id']
    table.delete_item(Key={'product_id': product_id})
    return {'statusCode': 200, 'body': 'Product deleted successfully'}


def get_all_products(event):
    response = table.scan()
    items = response.get('Items', [])
    return {'statusCode': 200, 'body': json.dumps(items)}
