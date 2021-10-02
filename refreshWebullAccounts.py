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
        '#U' : 'username',
        '#UID' : 'userId'
    }
    projection_expression = "#U, #UID"
    webull_accounts = dynamoClient.scan(
        ExpressionAttributeNames=expression_attribute_names,
        ProjectionExpression=projection_expression,
        TableName='WebullAccount'
    ).get("Items",[])
    try:
        for account in webull_accounts:
            username = getAttribute(account, 'username', 'S')
            userId = getAttribute(account, 'userId', 'S')
            print("Refreshing for user: {}".format(username))
            refresh_url = "https://ji1g9w5p36.execute-api.us-west-1.amazonaws.com/test/webull/refreshdata?username={}".format(username)
            refresh_url += "&userId=" + userId
            requests.request("GET", url=refresh_url)

    except Exception as e:
        print("Found error: {}".format(e))
        return {
            'statusCode': 400,
            'body': json.dumps(e)
        }
    return {
        'statusCode': 200,
        'body': json.dumps('Succesfully Refreshed data for webull accounts')
    }