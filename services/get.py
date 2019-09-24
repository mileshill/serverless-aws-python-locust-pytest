import json
import logging
import boto3
from http import HTTPStatus
from services.shared import TABLENAME
from services.shared import error_handler
logger = logging.getLogger(__file__)


@error_handler
def get(event, context):
    dynamo = boto3.client("dynamodb")
    get_result = dynamo.get_item(
        TableName=TABLENAME,
        Key={"name": event["pathParameters"]["name"]}  # Configured in YAML
    )
    assert get_result["Item"] is not None  # Item not found
    assert bool(get_result["Item"])  # Empty dict will fail
    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({
            "age": get_result["Item"]["age"]["N"],
            "name": get_result["Item"]["name"]["S"]
        })
    }
