import json
import logging
import boto3
from http import HTTPStatus
from services.shared import TABLENAME
from services.shared import error_handler
logger = logging.getLogger(__file__)


@error_handler
def delete(event, context):
    key_name = json.loads(event["body"])["name"]
    dynamo = boto3.client("dynamodb")
    dynamo.delete_item(
       TableName=TABLENAME,
       Key={"name": {"S": key_name}}
    )

    return {"statusCode": HTTPStatus.OK}
