from roboswag.validate.core import ValidateBase


class ValidateTextResponse(ValidateBase):
    def response_as_text(self, response, exp_response):
        self.logger.info("Validating response...")
        assertion_err_msg = (
            "Received response description:\n"
            f"    '{response.text}'\n"
            "does not equal expected:\n"
            f"    '{exp_response}'"
        )
        assert response.text == exp_response, assertion_err_msg
        self.logger.info("Response is valid.")
