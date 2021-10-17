import re
from collections import defaultdict
from itertools import chain
import yaml
from typing import List


class Parameter:
    def __init__(self, name, default=None):
        self.name = name
        self.python_name = pythonify_name(name)
        self.default = default

    def __str__(self):
        if self.default is None:
            return self.python_name
        return f"{self.python_name}={self.default}"


class Endpoint:
    def __init__(self, method_name, http_method, url, path_params: List[Parameter], headers: List[Parameter],
                 query: List[Parameter], body: List[Parameter]):
        self.method_name = method_name
        self.http_method = http_method
        self.url = self.prepare_path(url, path_params)
        self.path_params = path_params
        self.headers = headers
        self.query = query
        self.body = body
        self.method_signature = self.get_python_method_signature()

    @staticmethod
    def prepare_path(url, path_params):
        for param in path_params:
            url = url.replace(f"{{{param.name}}}", f"{{{param.python_name}}}")
        return url

    def get_python_method_signature(self):
        args = [str(param) for param in chain(self.path_params, self.headers, self.query, self.body)]
        args.append("exp_status=200")
        line = f"    def {self.method_name}(self"
        prefix = len(line) - 4
        last_index = len(args) - 1
        method_sig = ""
        for index, arg in enumerate(args):
            if not arg:
                continue
            if len(line) + len(arg) + 2 > 120 - (2 if last_index == index else 0):
                method_sig += line
                line = ",\n" + prefix * " " + arg
            else:
                line += f", {arg}"
        method_sig += line
        return method_sig


class Tag:
    def __init__(self, name):
        # tag is grouped paths/endpoints
        self.name = name
        self.endpoints = []


class APIModel:
    def __init__(self, name):
        self.name = name
        self.tags = {}

    @classmethod
    def from_swagger(cls, source):
        with open(source) as f:
            data = yaml.load(f, Loader=yaml.Loader)
        name = data["info"]["title"].replace(" ", "")
        api_model = cls(name)
        for path, path_body in data["paths"].items():
            for method, method_body in path_body.items():
                tag_name = method_body["tags"][0].strip(" -_").title() + "API"  # TODO: configurable class name
                unique_name = pythonify_name(method_body["operationId"])  # TODO fallback sicne its optional
                params = defaultdict(list)
                for param in method_body.get("parameters", []):
                    params[param["in"]].append(
                        Parameter(param["name"], default="None" if param["in"] != "path" else None)
                    )
                endpoint = Endpoint(unique_name, method, path, path_params=params["path"], headers=params["header"],
                                    query=params["query"], body=params["body"])
                api_model.add_endpoint_to_tag(tag_name, endpoint)
        return api_model

    def add_endpoint_to_tag(self, tag, endpoint):
        if tag not in self.tags:
            self.tags[tag] = Tag(tag)
        self.tags[tag].endpoints.appenmd(endpoint)


def pythonify_name(name):
    names = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", name)).split()
    name = "_".join(name.lower() for name in names)
    name = name.replace("-", "")
    return name
