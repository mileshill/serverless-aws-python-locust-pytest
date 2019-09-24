import json
import requests
import pytest
from collections import namedtuple
from enum import Enum
from configargparse import ArgumentParser

parser = ArgumentParser(default_config_files=["tests/test.conf"])
parser.add_argument("--lambda-uri", required=True, type=str, help="http://lambda.aws.com")
parser.add_argument("--lambda-api", required=True, type=str, help="/dev/v1/blah")
config = parser.parse_args()

Kitten = namedtuple("Kitten", "name age")
TEST_KITTEN = Kitten("Cleopatra", 3)



class Headers(Enum):
    APPLICATION_JSON = {"Content-Type": "application/json"}


class TestKittenCRUD:
    @pytest.fixture
    def url(self):
        return f"{config.lambda_uri}{config.lambda_api}"

    def test_post(self, url):
        body = {
            "name": TEST_KITTEN.name,
            "age": TEST_KITTEN.age
        }
        response = requests.post(url, json.dumps(body))
        assert response.status_code == 201

    def test_get_list(self, url):
        response = requests.get(url)
        assert len(response.json()) > 0

    def test_get_by_name(self, url):
        params = {"name": TEST_KITTEN.name}
        response = requests.get(url, params=params)
        assert int(response.json()[0]["age"]) == TEST_KITTEN.age

    def test_update_age_by_name(self, url):
        body = {"name": TEST_KITTEN.name, "age": TEST_KITTEN.age + 1}
        response = requests.put(url,  data=json.dumps(body))
        assert response.status_code == 200

    def test_delete(self, url):
        data = {"name": TEST_KITTEN.name}
        response = requests.delete(url, data=json.dumps(data))
        assert response.status_code == 200
