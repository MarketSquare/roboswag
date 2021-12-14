from openapi.generate.utils import pythonify_name


class Parameter:
    def __init__(self, name: str, default=None) -> None:
        self.name: str = name
        self.python_name: str = pythonify_name(name)
        self.default = default

    def __str__(self):
        if self.default is None:
            return self.python_name
        return f"{self.python_name}={self.default}"
