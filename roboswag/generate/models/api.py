import re
from collections import defaultdict
from typing import Dict

import yaml
from prance import ResolvingParser
from prance.convert import convert_spec

from roboswag.generate.models.definition import Definition, Property
from roboswag.generate.models.endpoint import Endpoint
from roboswag.generate.models.parameter import Parameter
from roboswag.generate.models.response import Response
from roboswag.generate.models.tag import Tag
from roboswag.generate.models.utils import get_python_type, pythonify_name


class APIModel:
    def __init__(self) -> None:
        self.name: str = ""
        self.tags: Dict[str, Tag] = {}
        self.definitions: Dict[str, Definition] = {}

    def parse_swagger(self, swagger):
        self.parse_info(swagger)
        self.parse_paths(swagger)
        self.parse_tags(swagger)
        self.parse_definitions(swagger)

    def parse_info(self, swagger):
        name = swagger["info"]["title"].replace(" ", "")
        self.name = name

    def get_unique_endpoint_name(self, path, method, method_body):
        if "operationId" in method_body:
            return pythonify_name(method_body["operationId"])
        # split on camelCase and / path
        parts = re.split("((?<=[a-z])(?=[A-Z])|/)", path)
        name = method
        for part in parts:
            part = re.sub("[/{}]", "", part)
            part = part.replace("-", "_")
            if not part:
                continue
            name += f"_{part.lower()}"
        return name

    @staticmethod
    def class_name_from_tag(method_body, **kwargs):
        return method_body["tags"][0].strip(" -_").title()

    @staticmethod
    def class_name_from_path(path, **kwargs):
        for part in path.split("/"):
            part = re.sub("[/{}]", "", part)
            if not part:
                continue
            return part.title()

    def set_source_of_class_name(self, swagger):
        """
        If all methods have their tags - use tag name. Otherwise use first part of the path.
        """
        # TODO configurable class name
        for path_body in swagger["paths"].values():
            for method in path_body.values():
                if "tag" not in method:
                    return self.class_name_from_path
        return self.class_name_from_tag

    def parse_paths(self, swagger):
        get_class_name = self.set_source_of_class_name(swagger)
        for path, path_body in swagger["paths"].items():
            method: str
            method_body: Dict
            for method, method_body in path_body.items():
                class_name = get_class_name(path=path, method_body=method_body)
                unique_name = self.get_unique_endpoint_name(path, method, method_body)
                summary = method_body.get("summary", "")
                description = method_body.get("description", "")
                params = defaultdict(list)
                for param in method_body.get("parameters", []):
                    params[param["in"]].append(
                        Parameter(
                            param["name"],
                            default="None" if param["in"] != "path" else None,  # TODO Retrieve default value
                            param_type=get_python_type(param["type"], param.get("format"))
                            if param.get("type")
                            else None,
                            description=param.get("description"),
                            required=param.get("required"),
                            schema=param.get("schema"),
                        )
                    )
                responses = dict()
                for status_code, resp in method_body.get("responses", []).items():
                    responses[status_code] = Response(
                        description=resp.get("description"),
                        headers=resp.get("headers"),
                        schema=resp.get("schema"),
                    )
                body = params["body"][0] if params["body"] else None
                endpoint = Endpoint(
                    unique_name,
                    method,
                    path,
                    summary=summary,
                    description=description,
                    path_params=params["path"],
                    headers=params["header"],
                    query=params["query"],
                    body=body,
                    responses=responses,
                )
                self.add_endpoint_to_tag(class_name, endpoint)

    def parse_tags(self, swagger):
        if not swagger.get("tags"):
            return
        for tag in swagger["tags"]:
            tag_name = Tag.normalize_tag_name(tag["name"])
            if tag_name in self.tags:
                self.tags[tag_name].description = tag["description"]

    def add_endpoint_to_tag(self, tag: str, endpoint: Endpoint) -> None:
        if tag not in self.tags:
            self.tags[tag] = Tag(tag)
        self.tags[tag].endpoints.append(endpoint)

    def parse_definitions(self, swagger):
        for def_name, def_body in swagger["definitions"].items():
            def_type = def_body.get("type", "")
            def_req = def_body.get("required")
            properties = []
            for prop_name, prop_body in def_body.get("properties", {}).items():
                prop_type = prop_body.get("type", "")
                prop_format = prop_body.get("format", "")
                properties.append(Property(prop_name, prop_type=get_python_type(prop_type, prop_format)))

            definition = Definition(def_name, def_type=def_type, properties=properties, required=def_req)
            self.definitions[def_name] = definition


class APIModelCreator:
    @staticmethod
    def from_yaml(source):
        with open(source) as f:
            data = yaml.load(f, Loader=yaml.Loader)
        api_model = APIModel()
        api_model.parse_swagger(data)
        return api_model, data

    @staticmethod
    def from_prance(source, convert_to_3=False):
        # TODO: support for swagger 3.0 (https://swagger.io/specification/)
        parser = ResolvingParser(source)
        swagger = parser.specification
        # convert to OpenAPI 3.x if swagger is in version 2.x
        if swagger.get("swagger") and convert_to_3:
            swagger = convert_spec(swagger).specification
        api_model = APIModel()
        api_model.parse_swagger(swagger)
        return api_model, swagger
