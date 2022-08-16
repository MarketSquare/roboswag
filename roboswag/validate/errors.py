from roboswag.validate.core import ValidateBase


class ValidateError(ValidateBase):
    @staticmethod
    def error(response, exp_error):
        assertion_err_msg = (
            f"Received response description:\n    '{response.text}'\n" f"does not equal expected:\n    '{exp_error}'"
        )
        assert response.text == exp_error, assertion_err_msg
