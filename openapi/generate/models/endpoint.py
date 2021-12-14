from itertools import chain
from typing import List

from openapi.generate.models.parameter import Parameter


class Endpoint:
    def __init__(
        self,
        method_name: str,
        http_method,
        url,
        path_params: List[Parameter],
        headers: List[Parameter],
        query: List[Parameter],
        body: List[Parameter],
    ):
        self.method_name: str = method_name
        self.http_method = http_method
        self.url = self.prepare_path(url, path_params)
        self.path_params: List[Parameter] = path_params
        self.headers: List[Parameter] = headers
        self.query: List[Parameter] = query
        self.body: List[Parameter] = body
        self.method_signature: str = self.get_python_method_signature()

    @staticmethod
    def prepare_path(url, path_params):
        for param in path_params:
            url = url.replace(f"{{{param.name}}}", f"{{{param.python_name}}}")
        return url

    def get_python_method_signature(self) -> str:
        max_line_length: int = 120
        args = [str(param) for param in chain(self.path_params, self.headers, self.query, self.body)]
        args.append("exp_status=200")  # TODO handle different status codes & reading them from swagger
        line = f"    def {self.method_name}(self"
        prefix = len(line) - 4
        last_index = len(args) - 1
        method_sig = ""
        for index, arg in enumerate(args):
            if not arg:
                continue
            if len(line) + len(arg) + 2 > max_line_length - (2 if last_index == index else 0):
                method_sig += line
                line = ",\n" + prefix * " " + arg
            else:
                line += f", {arg}"
        method_sig += line
        return method_sig
