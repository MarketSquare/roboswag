from itertools import chain
from typing import Dict, List

from roboswag.generate.models.parameter import Parameter
from roboswag.generate.models.response import Response


class Endpoint:
    def __init__(
        self,
        method_name: str,
        http_method,
        url,
        summary: str,
        description: str,
        path_params: List[Parameter],
        headers: List[Parameter],
        query: List[Parameter],
        body: Parameter,
        responses: Dict[str, Response],
        exp_status: str = "200",
    ):
        self.method_name: str = method_name
        self.http_method = http_method
        self.url = self.prepare_path(url, path_params)
        self.summary: str = summary
        self.description: str = description
        self.path_params: List[Parameter] = path_params
        self.headers: List[Parameter] = headers
        self.query: List[Parameter] = query
        self.body: Parameter = body
        self.responses: Dict[str, Response] = responses
        self.exp_status = exp_status
        self.method_signature: str = self.get_python_method_signature()

    @staticmethod
    def prepare_path(url, path_params):
        for param in path_params:
            url = url.replace(f"{{{param.name}}}", f"{{{param.python_name}}}")
        return url

    def get_python_method_signature(self) -> str:
        max_line_length: int = 120
        args = [str(param) for param in chain(self.path_params, self.headers, self.query) if param]
        if self.body:
            args.append(f"{self.body}")
        args.append(f"exp_status={self.exp_status}")
        args.append(f"validate_schema=True")
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
