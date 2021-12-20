from typing import List

from openapi.generate.models.utils import get_python_type, pythonify_name


class Property:
    def __init__(self, name: str, prop_type=None):
        self.name: str = pythonify_name(name)
        self.type = prop_type


class Definition:
    def __init__(self, name: str, def_type, properties: List[Property]):
        self.name: str = name
        self.type = get_python_type(def_type)
        self.properties: List[Property] = properties
