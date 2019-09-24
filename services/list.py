import json
import logging
import boto3
from http import HTTPStatus
from services.shared import TABLENAME
from services.shared import error_handler
logger = logging.getLogger(__file__)


@error_handler
def list(event, context):
    dynamo = boto3.client("dynamodb")
    scan_results = dynamo.scan(TableName=TABLENAME)

    # Check for content returned. If no content, 404
    scanned_items = scan_results["Items"]
    assert len(scanned_items) > 0

    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps([
            {
                "name": kitten["name"]["S"],
                "age": kitten["age"]["N"]
            } for kitten in scan_results["Items"]
        ])
    }

