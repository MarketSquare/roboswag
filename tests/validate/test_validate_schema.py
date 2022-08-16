import json
from pathlib import Path
from unittest.mock import Mock

import jsonschema
import pytest

from roboswag.validate import Validate

TEST_DATA = Path(__file__).parent / "test_data"
VALID_SCHEMA = TEST_DATA / "valid_schema.json"
INVALID_SCHEMA = TEST_DATA / "invalid_schema.json"
INVALID_SCHEMA_JSON = TEST_DATA / "invalid_schema_json.json"


@pytest.fixture
def validator():
    logger = Mock()
    return Validate(logger=logger)


@pytest.fixture
def valid_response():
    return {"code": 123, "type": "abc", "message": "abc"}


@pytest.fixture
def invalid_response():
    return {"code": "123"}


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
