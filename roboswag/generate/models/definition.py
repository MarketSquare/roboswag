from typing import List

from roboswag.generate.models.utils import get_python_type, pythonify_name, replace_reserved_name


class Property:
    def __init__(self, name: str, prop_type=None):
        self.name: str = replace_reserved_name(pythonify_name(name))
        self.type = prop_type


class Definition:
    def __init__(self, name: str, def_type, properties: List[Property], required=None):
        self.name: str = name
        self.type = get_python_type(def_type)
        self.required = required
        self.properties: List[Property] = properties


def get_definitions_from_swagger(swagger):
    """
    Get resolved schema definition from Swagger file. Supports both OpenAPI v2 and 3.
    """
    return swagger.get("definitions", swagger.get("components", {}).get("schemas", {}))
