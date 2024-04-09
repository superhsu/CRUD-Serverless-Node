# CRUD serverless workshop

This workshop contains instructions on how to create a CRUD NodeJS application that will function as a shopping list → you can add, remove or get products on the shopping list.

## CRUD workshop flow diagram 

<img width="1190" alt="flow" src="https://github.com/superhsu/CRUD-Serverless-Node/assets/31141265/e066a0d6-da65-441b-bbf9-089868f592f2">

## Workshop Prerequisites

- AWS account
- AWS CLI configured 
- Datadog API Key 

## Getting Started 

### Create the Lambda function 

Create the NodeJS/Python Lambda function by copying and pasting the code found in the NodeJS/Python directory to the Lambda code source(Suggested runtime version Node.js 16.x/Python 3.12). 

Add the following permissions policies to the Lambda role: 

- **AmazonDynamoDBFullAccess**
- **CloudWatchLogsFullAccess**

### Create the DynamoDB table

Create the DynamoDB table by following the guided AWS UI create table steps(use the default settings and put any string as the partition key e.g. "productId"). 

**In the Lambda function code source find the "dynamodbTableName"(NodeJS) or "table_name"(Python) variable name and replace the value with the DynamoDB table name you just created.** 

### Create the API Gateway 

Create a REST API Gateway(leave the API endpoint type as regional). 

Create three resource endpoints from the root path(/). Enable CORS for each resource endpoint. Then create the method requests for each endpoint shown in the bullet points below. 

For each method request select "Lambda Function" as the integration type, enable Lambda proxy integration, select the correct region, and enter the Lambda function you created then create the function(leave the rest of the default settings as is) 

- /health

  - GET 

- /product

  - GET
  - POST
  - PATCH
  - DELETE

- /products 

  - GET

Your API Gateway should look like the image below: 

<img width="334" alt="Screenshot 2024-04-08 at 7 54 57 PM" src="https://github.com/superhsu/CRUD-Serverless-Workshop/assets/31141265/bc35c320-1b7d-4ca8-8482-2aead6098b41">

### Test the Lambda

Send API requests to invoke the Lambda function 

```
curl -X GET '<API DOMAIN/health>' 

curl -X POST '<API DOMAIN/product>' \
  -d '{
        "inventory": 2000,
        "price": 80,
        "color": "dark",
        "productid": "10",
        "productName": "serverless bits"
      }'

curl -X GET '<API DOMAIN/products>'

```

### Instrument the Lambda function using Datadog

**This step requires the AWS CLI to be installed and configured on your machine/VM** 

[Datadog AWS Lambda documentation](https://docs.datadoghq.com/serverless/aws_lambda/installation/)

1. Install the Datadog CLI client 

```
npm install -g @datadog/datadog-ci
```

2. Launch the Datadog CLI in the interactive mode to guide your first installation for a quick start

```
datadog-ci lambda instrument -i
```

3. Select the region where the Lambda function is deployed e.g. "us-west-1" 

4. Select your Datadog instance e.g. "datadoghq.com"

5. Enter your Datadog API key 

6. Select the Lambda function you'd like to instrument 

The Datadog CLI will attach the Datadog library and extension layers and set the required environment variables to the Lambda function. 

### Invoke the Lambda functions to view the Lambda function metrics and traces in Datadog

<img width="1483" alt="Screenshot 2024-04-08 at 10 14 55 PM" src="https://github.com/superhsu/CRUD-Serverless-Workshop/assets/31141265/3c535304-916b-47f5-90ea-fa5c22be8b23">
<img width="1502" alt="Screenshot 2024-04-08 at 10 15 33 PM" src="https://github.com/superhsu/CRUD-Serverless-Workshop/assets/31141265/51b3e09d-588c-4cc4-af9f-2a5221fd9586">




