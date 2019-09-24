import json
import logging
import boto3
from http import HTTPStatus
from services.shared import TABLENAME
from services.shared import error_handler
logger = logging.getLogger(__file__)


@error_handler
def update(event, context):
    # Validate the json
    print(event["body"])
    new_item = json.loads(event["body"])

    # Validate the kitten object
    assert new_item["age"] is not None
    assert int(new_item["age"]) > -1

    dynamo = boto3.client("dynamodb")
    dynamo.update_item(
        TableName=TABLENAME,
        Key={"name": {"S": new_item["name"]}},
        UpdateExpression="set #age = :age",
        ExpressionAttributeNames={"#age": "age"},  # Column name
        ExpressionAttributeValues={":age": {"N": str(new_item["age"])}}  # Value for column
    )
    return {"statusCode": HTTPStatus.OK}

