import json
import logging
import boto3
from http import HTTPStatus
from services.shared import Kitten
from services.shared import TABLENAME
from services.shared import error_handler
logger = logging.getLogger(__file__)


@error_handler
def create(event, context):
    """
    Create an item
    :param event:
    :param context:
    :return:
    """
    # Validate the json
    kitten = Kitten(**json.loads(event["body"]))
    # Create new kitten in database
    dynamo = boto3.client("dynamodb")
    dynamo.put_item(
        TableName=TABLENAME,
        Item={
            "name": {"S": kitten.name},
            "age": {"N": str(kitten.age)}
        }
    )
    return {"statusCode": HTTPStatus.CREATED}

