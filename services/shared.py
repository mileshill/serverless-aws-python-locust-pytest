import os
from http import HTTPStatus
from collections import namedtuple
from json import JSONDecodeError

Kitten = namedtuple("Kitten", "name age")
TABLENAME = os.environ["DYNAMODB_KITTEN_TABLE"]


def status_code(code):
    return {"statusCode": code}


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
           results = func(*args, **kwargs)
        except (KeyError, ValueError, JSONDecodeError) as e:
            print(e)
            return status_code(HTTPStatus.BAD_REQUEST)
        except AttributeError as e:
            print(e)
            return status_code(HTTPStatus.INTERNAL_SERVER_ERROR)
        except AssertionError as e:
            print(e)
            return status_code(HTTPStatus.NOT_FOUND)
        except Exception as e:
            print(e)
            return status_code(HTTPStatus.SERVICE_UNAVAILABLE)
        return results
    return wrapper
