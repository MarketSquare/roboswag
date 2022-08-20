from unittest.mock import Mock

import pytest

from roboswag.validate import Validate


@pytest.fixture
def validator():
    logger = Mock()
    return Validate(logger=logger)


EXPECTED_TEXT = "I am being expected"


@pytest.fixture
def valid_text():
    response = Mock()
    response.text = EXPECTED_TEXT
    return response


@pytest.fixture
def invalid_text():
    response = Mock()
    response.text = "Not sure where I came from"
    return response


def test_valid_response_text(validator, valid_text):
    validator.response_as_text(valid_text, EXPECTED_TEXT)


def test_invalid_response(validator, invalid_text):
    exp_msg = (
        f"Received response description:\n    '{invalid_text.text}'\n"
        f"does not equal expected:\n"
        f"    '{EXPECTED_TEXT}'"
    )
    with pytest.raises(AssertionError, match=exp_msg):
        validator.response_as_text(invalid_text, EXPECTED_TEXT)
