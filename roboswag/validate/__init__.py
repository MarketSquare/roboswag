from roboswag.validate.errors import ValidateError
from roboswag.validate.schema import ValidateSchema


class Validate(ValidateSchema, ValidateError):
    pass
