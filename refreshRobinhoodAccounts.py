import json
import requests
import boto3

dynamoClient = boto3.client("dynamodb")
def getAttribute(dbItem, attributeName, attributeType):
    """
    INPUT
    dbItem: the databse item returned => {'headers' : {'S': 'some string'}, ...}
    attribtueName: name of the item
    attributeType: one of the dynamoDb datatypes => {'S', 'N'...}

    OUTPUT
    return database attribute 
    """
    return dbItem.get(attributeName, {}).get(attributeType, "")

def lambda_handler(event, context):
    # TODO implement
    expression_attribute_names = {
        '#U' : 'username'
    }
    projection_expression = "#U"
    robinhood_accounts = dynamoClient.scan(
        ExpressionAttributeNames=expression_attribute_names,
        ProjectionExpression=projection_expression,
        TableName='robinhoodAccount'
    ).get("Items",[])
    try:
        for account in robinhood_accounts:
            username = getAttribute(account, 'username', 'S')
            print("Refreshing for user: {}".format(username))
            refresh_url = "https://ji1g9w5p36.execute-api.us-west-1.amazonaws.com/test/robinhood/refreshdata/{}".format(username)
            requests.request("GET", url=refresh_url)

    except Exception as e:
        print("Found error: {}".format(e))
        return {
            'statusCode': 400,
            'body': json.dumps(e)
        }
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }