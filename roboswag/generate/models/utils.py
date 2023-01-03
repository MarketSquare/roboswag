import datetime
import re
import uuid
from typing import Dict

RESERVED_WORDS = {"global", "cls", "self"}

types_mapping = {
    "string": {
        "": str,
        "byte": str,
        "password": str,
        "date": datetime.date,
        "date-time": datetime.datetime,
        "binary": bytes,
        "uuid": uuid.UUID,
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


def pythonify_name(name: str, join_mark: str = "_", join_fn: str = "lower") -> str:
    names = re.split("([A-Z][a-z]+)", name)
    if join_fn == "lower":
        name = join_mark.join(name.lower() for name in names if name.strip())
    elif join_fn == "title":
        name = join_mark.join(name.title() for name in names if name.strip())
    name = name.replace("-", "")
    return name


def replace_reserved_name(name: str) -> str:
    """If the name is in reserved words, append it with _"""
    if name in RESERVED_WORDS:
        return f"_{name}"
    return name
