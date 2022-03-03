from roboswag.generate.models.utils import pythonify_name


class Parameter:
    def __init__(self, name: str, default=None, param_type=None, description=None, required=None, schema=None) -> None:
        self.name: str = name
        self.python_name: str = pythonify_name(name)
        self.default = default
        self.param_type = param_type
        self.description = description
        self.required = required
        self.schema = schema

    def __str__(self):
        if self.default is None:
            return self.python_name
        return f"{self.python_name}={self.default}"
