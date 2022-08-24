import json
from pathlib import Path
from typing import Any, Optional

import black
from jinja2 import Template

from roboswag.generate.models.api import get_definitions_from_swagger, parse_swagger_specification


class LibraryGenerator:
    def __init__(self, source, output: Optional[Path], authentication):
        self.source = source
        self.parent_dir = Path(__file__).parent
        api_model, swagger = parse_swagger_specification(self.source)
        self.api_model = api_model
        self.swagger = swagger
        self.output_dir = self.resolve_output_dir(output)
        self.default_auth = authentication
        self.unformatted_files = []

    def resolve_output_dir(self, output: Optional[Path]):
        output_dir = self.api_model.name
        if output is None:
            return Path(output_dir)
        return output / output_dir

    def generate(self):
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.generate_init()
        self.generate_endpoints()
        self.generate_models()
        self.generate_schemas()
        self.format_files()

    def format_files(self):
        for path in self.unformatted_files:
            blackify_file(path)
        self.unformatted_files = []

    def generate_init(self):
        swagger_version = self.swagger.get("openapi") or self.swagger.get("swagger")
        api_init_template = self.parent_dir / "templates" / "api_init.jinja"
        with open(api_init_template) as f:
            template = Template(f.read()).render(swagger_version=swagger_version, infos=self.swagger["info"])
        init_file = self.output_dir / "__init__.py"
        with open(init_file, "w") as f:
            f.write(template)
        print(f"Generated '{init_file}' file")
        self.unformatted_files.append(init_file)

    def get_api_auth(self):
        if self.default_auth is None:
            return self.api_model.authentication
        if self.default_auth == "disable":
            return None
        return self.default_auth

    def generate_endpoints(self):
        endpoints_dir = self.output_dir / "endpoints"
        Path(endpoints_dir).mkdir(exist_ok=True)
        print("Generating endpoints...")
        for tag in self.api_model.tags.values():
            paths_template = self.parent_dir / "templates" / "paths.jinja"
            with open(paths_template) as f:
                template = Template(f.read()).render(
                    class_name=tag.name,
                    authentication=self.get_api_auth(),
                    endpoints=tag.endpoints,
                    description=tag.description,
                )
            endpoint_file = endpoints_dir / f"{tag.name}.py"
            with open(endpoint_file, "w") as f:
                f.write(template)
            print(f"Generated '{endpoint_file}' file")
            self.unformatted_files.append(endpoint_file)

    def generate_models(self):
        models_dir = self.output_dir / "models"
        Path(models_dir).mkdir(exist_ok=True)
        print("Generating models...")
        for definition in self.api_model.definitions.values():
            models_template = self.parent_dir / "templates" / "models.jinja"
            with open(models_template) as f:
                template = Template(f.read()).render(class_name=definition.name, properties=definition.properties)
            model_file = models_dir / f"{definition.name}.py"
            with open(model_file, "w") as f:
                f.write(template)
            print(f"Generated '{model_file}' file")
            self.unformatted_files.append(model_file)

    def generate_schemas(self):
        schemas_dir = self.output_dir / "schemas"
        Path(schemas_dir).mkdir(exist_ok=True)
        print("Generating schemas...")
        schemas = get_definitions_from_swagger(self.swagger)
        for schema_name, schema in schemas.items():
            schema_file = schemas_dir / f"{schema_name}.json"
            with open(schema_file, "w") as f:
                f.write(json.dumps(schema, indent=4))
                f.write("\n")
            print(f"Generated '{schema_file}' file")
            self.unformatted_files.append(schema_file)


def blackify_file(source):
    black.format_file_in_place(source, fast=True, mode=black.FileMode(), write_back=black.WriteBack.YES)


def generate_libraries(source: str, output_dir: Optional[Path], authentication: Any):
    generator = LibraryGenerator(source, output_dir, authentication)
    generator.generate()
