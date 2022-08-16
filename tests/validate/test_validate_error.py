from pathlib import Path
from unittest.mock import Mock

import pytest

from roboswag.validate import Validate


@pytest.fixture
def validator():
    logger = Mock()
    return Validate(logger=logger)


EXPECTED_ERROR = "I am being expected"


@pytest.fixture
def valid_error():
    response = Mock()
    response.text = EXPECTED_ERROR
    return response


@pytest.fixture
def invalid_error():
    response = Mock()
    response.text = "Not sure where I came from"
    return response


def test_valid_error(validator, valid_error):
    validator.error(valid_error, EXPECTED_ERROR)


def test_invalid_error(validator, invalid_error):
    exp_msg = (
        f"Received response description:\n    '{invalid_error.text}'\n"
        f"does not equal expected:\n"
        f"    '{EXPECTED_ERROR}'"
    )
    with pytest.raises(AssertionError, match=exp_msg):
        validator.error(invalid_error, EXPECTED_ERROR)
