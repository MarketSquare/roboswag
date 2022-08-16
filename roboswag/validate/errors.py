from roboswag.validate.core import ValidateBase


class ValidateError(ValidateBase):
    def error(self, response, exp_error):
        self.logger.info("Validating error message...")
        assertion_err_msg = (
            f"Received response description:\n    '{response.text}'\n" f"does not equal expected:\n    '{exp_error}'"
        )
        assert response.text == exp_error, assertion_err_msg
        self.logger.info("Error message is valid.")
