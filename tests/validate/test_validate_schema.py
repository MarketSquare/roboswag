import json
from pathlib import Path
from unittest.mock import Mock

import jsonschema
import pytest

from roboswag.validate import ValidateSchema

TEST_DATA = Path(__file__).parent / "test_data"
VALID_SCHEMA = TEST_DATA / "valid_schema.json"
INVALID_SCHEMA = TEST_DATA / "invalid_schema.json"
INVALID_SCHEMA_JSON = TEST_DATA / "invalid_schema_json.json"


@pytest.fixture
def validator():
    logger = Mock()
    return ValidateSchema(logger=logger)


@pytest.fixture
def valid_response():
    response = Mock()
    response_json = {"code": 123, "type": "abc", "message": "abc"}
    response.json = Mock(return_value=response_json)
    return response


@pytest.fixture
def invalid_response():
    response = Mock()
    response.json = Mock(return_value={"code": "123"})
    return response


def test_validate_valid_schema_path(validator, valid_response):
    validator.schema(valid_response, VALID_SCHEMA)


def test_validate_valid_schema(validator, valid_response):
    with open(VALID_SCHEMA) as fp:
        schema = json.load(fp)
    validator.schema(valid_response, schema)


@pytest.mark.skip("Missing error handling")
def test_validate_invalid_schema_json(validator, valid_response):
    # FIXME add error handling (raises JSOnDecodeError)
    validator.schema(valid_response, INVALID_SCHEMA_JSON)


@pytest.mark.skip("Missing error handling")
def test_validate_invalid_schema(validator, valid_response):
    # Raises jsonschema.exceptions.SchemaError: 'unknown' is not valid under any of the given schemas
    validator.schema(valid_response, INVALID_SCHEMA)


def test_validate_invalid_response(validator, invalid_response):
    # TODO: Custom exception from Roboswag (with error stack on debug only)
    with pytest.raises(jsonschema.exceptions.ValidationError, match="'123' is not of type 'integer'"):
        validator.schema(invalid_response, VALID_SCHEMA)
