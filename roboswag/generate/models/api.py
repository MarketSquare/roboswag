import re
from collections import defaultdict
from typing import Dict, Optional

from prance import ResolvingParser
from prance.convert import convert_spec

from roboswag.generate.models.definition import Definition, Property, get_definitions_from_swagger
from roboswag.generate.models.endpoint import Endpoint
from roboswag.generate.models.parameter import Parameter
from roboswag.generate.models.response import Response
from roboswag.generate.models.tag import Tag
from roboswag.generate.models.utils import get_python_type, pythonify_name


def get_schema(param):
    return param.get("schema") or get_schema_openapi_v3(param)


def get_schema_openapi_v3(param):
    return param.get("content", {}).get("application/json", {}).get("schema", {})


def get_body(params, method_body):
    """
    Get optional body of the request.
    For OpenAPI v2 body is part of the parameters (with in: body).
    For OpenAPi v3 body is in separate property requestBody.
    # TODO: We only support application/json type of the body
    """
    if "body" in params:
        # TODO Can it be more than one? If not, should we use the same container as for headers & query?
        return params["body"][0]
    if "requestBody" in method_body:
        schema = get_schema_openapi_v3(method_body["requestBody"])
        if not schema:
            return None
        return Parameter(
            "body", default="None", param_type=None, description=None, required=None, schema=schema  # TODO
        )


class APIModel:
    def __init__(self) -> None:
        self.name: str = ""
        self.tags: Dict[str, Tag] = {}
        self.definitions: Dict[str, Definition] = {}
        self.authentication: Optional[str] = None

    def parse_swagger(self, swagger):
        self.parse_info(swagger)
        self.parse_paths(swagger)
        self.parse_tags(swagger)
        self.parse_schemas(swagger)
        self.parse_authentication(swagger)

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
        return "Root"

    def set_source_of_class_name(self, swagger):
        """
        If all methods have their tags - use tag name. Otherwise use first part of the path.
        """
        # TODO configurable class name
        for path_body in swagger["paths"].values():
            for method in path_body.values():
                if "tags" not in method:
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
                            schema=get_schema(param),
                        )
                    )
                responses = dict()
                for status_code, resp in method_body.get("responses", []).items():
                    responses[status_code] = Response(
                        description=resp.get("description"),
                        headers=resp.get("headers"),
                        schema=get_schema(resp),
                    )
                body = get_body(params, method_body)
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

    def parse_schemas(self, swagger):
        schemas = get_definitions_from_swagger(swagger)
        for def_name, def_body in schemas.items():
            def_type = def_body.get("type", "")
            def_req = def_body.get("required")
            properties = []
            for prop_name, prop_body in def_body.get("properties", {}).items():
                prop_type = prop_body.get("type", "")
                prop_format = prop_body.get("format", "")
                properties.append(Property(prop_name, prop_type=get_python_type(prop_type, prop_format)))

            definition = Definition(def_name, def_type=def_type, properties=properties, required=def_req)
            self.definitions[def_name] = definition

    def parse_authentication(self, swagger):
        # TODO we should check what security schemes applies to which endpoints
        # it could be that entire path does not need auth, while other needs it etc
        security_schemes = swagger.get("components", {}).get("securitySchemes", {})
        if not security_schemes:
            return
        for name, scheme in security_schemes.items():
            if scheme.get("type", "") == "http" and scheme.get("scheme", "") == "basic":
                self.authentication = "BasicAuth"
                return


def parse_swagger_specification(source, convert_to_3=False):
    def recursion_limit_handler(limit, refstring, recursions):
        return {}

    parser = ResolvingParser(
        source,
        backend="openapi-spec-validator",
        recursion_limit=1,
        recursion_limit_handler=recursion_limit_handler,
    )
    swagger = parser.specification
    # convert to OpenAPI 3.x if swagger is in version 2.x
    if swagger.get("swagger") and convert_to_3:
        swagger = convert_spec(swagger).specification
    api_model = APIModel()
    api_model.parse_swagger(swagger)
    return api_model, swagger
