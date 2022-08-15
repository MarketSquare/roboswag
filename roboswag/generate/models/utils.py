import datetime
import re
from typing import Dict

types_mapping = {
    "string": {
        "": str,
        "byte": str,
        "password": str,
        "date": datetime.date,
        "date-time": datetime.datetime,
        "binary": bytes,
    },
    "integer": {
        "": int,
        "int32": int,
        "int64": int,
    },
    "number": {
        "float": float,
        "double": float,
    },
    "boolean": bool,
    "file": "file",
    "array": list(),
    "object": object,
}


def get_python_type(param_type, param_format=None):
    if not param_type:
        return str
    if not types_mapping[param_type]:
        return str
    if not isinstance(types_mapping[param_type], Dict):
        return types_mapping[param_type]
    if param_format:
        return types_mapping[param_type][param_format]
    return str


def pythonify_name(name: str) -> str:
    names = re.split("([A-Z][a-z]+)", name)
    name = "_".join(name.lower() for name in names if name.strip())
    name = name.replace("-", "")
    return name
