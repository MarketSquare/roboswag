from collections import defaultdict
from typing import Dict

import yaml

from openapi.generate.models.endpoint import Endpoint
from openapi.generate.models.parameter import Parameter
from openapi.generate.models.tag import Tag
from openapi.generate.utils import pythonify_name


class APIModel:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.tags: Dict[str, Tag] = {}

    @classmethod
    def from_swagger(cls, source):
        with open(source) as f:
            data = yaml.load(f, Loader=yaml.Loader)
        name = data["info"]["title"].replace(" ", "")
        api_model = cls(name)

        for path, path_body in data["paths"].items():
            for method, method_body in path_body.items():
                tag_name = method_body["tags"][0].strip(" -_").title() + "API"  # TODO configurable class name
                unique_name = pythonify_name(method_body["operationId"])  # TODO fallback since its optional
                params = defaultdict(list)
                for param in method_body.get("parameters", []):
                    params[param["in"]].append(
                        Parameter(
                            param["name"],
                            default="None" if param["in"] != "path" else None,  # TODO Retrieve default value
                        )
                    )
                endpoint = Endpoint(
                    unique_name,
                    method,
                    path,
                    path_params=params["path"],
                    headers=params["header"],
                    query=params["query"],
                    body=params["body"],
                )
                api_model.add_endpoint_to_tag(tag_name, endpoint)

        for tag in data["tags"]:
            tag_name = Tag.normalize_tag_name(tag["name"])
            if tag_name in api_model.tags:
                api_model.tags[tag_name].description = tag["description"]

        return api_model

    def add_endpoint_to_tag(self, tag: str, endpoint: Endpoint) -> None:
        if tag not in self.tags:
            self.tags[tag] = Tag(tag)
        self.tags[tag].endpoints.append(endpoint)
