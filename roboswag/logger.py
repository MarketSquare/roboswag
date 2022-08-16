from pprint import pformat

from robot.api import logger


class Logger:
    @staticmethod
    def info(message):
        logger.info(message)

    @staticmethod
    def debug(message):
        logger.debug(message)

    @staticmethod
    def log_request(response):
        # TODO we can add flag for removing auth details (such as passwords, tokens) if needed
        if response.history:  # TODO print redirects
            original_request = response.history[0].request
            redirected = "(redirected)"
        else:
            original_request = response.request
            redirected = ""
        logger.info(
            f"{original_request.method.upper()} {original_request.url} {redirected}\n"
            f"headers: {pformat(original_request.headers)}"
        )  # TODO make pretty print work

    @staticmethod
    def log_response(response):
        logger.info(f"{response.request.method.upper()} response: {response.status_code} {response.text}")
