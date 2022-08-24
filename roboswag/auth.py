from requests.auth import HTTPBasicAuth
from robot.libraries.BuiltIn import BuiltIn


class MissingParameter(ValueError):
    def __init__(self, name):
        super().__init__(f"Missing {name}. Set ${{{name}}} global variable or pass it as {name} named variable.")


def get_from_kwargs_or_robot(kwargs, name, missing_ok=True):  # TODO pass flag to enforce auth with missing_ok
    value = kwargs.get(name)
    if value is None:
        value = BuiltIn().get_variable_value(f"${{{name}}}")
    if not missing_ok and value is None:
        raise MissingParameter(name) from None
    return value


class TokenHandler:
    # FIXME
    def __init__(self, **kwargs):
        self.access_token = get_from_kwargs_or_robot(kwargs, "access_token")

    def __call__(self, *args, **kwargs):
        user = get_from_kwargs_or_robot(kwargs, "user")
        password = get_from_kwargs_or_robot(kwargs, "password")
        super().__init__(user, password)


class BasicAuth(HTTPBasicAuth):
    def __init__(self, **kwargs):
        user = get_from_kwargs_or_robot(kwargs, "user")
        password = get_from_kwargs_or_robot(kwargs, "password")
        super().__init__(user, password)


AUTH_BACKENDS = {
    "disable": "disable",
    "basicauth": "BasicAuth",
}
