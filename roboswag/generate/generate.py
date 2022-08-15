import json
from pathlib import Path
from typing import List, Optional

import black
from jinja2 import Template

from roboswag.generate.models.api import APIModelCreator
from roboswag.generate.models.definition import Definition


def generate_libraries(source, output: Optional[Path] = None):
    api_model, swagger = APIModelCreator.from_prance(source)
    output_dir = api_model.name
    if output is not None:
        output_dir = output / output_dir
    Path(output_dir).mkdir(exist_ok=True)

    init_files = generate_init(swagger, output_dir)
    blackify_files(init_files)

    endpoints_dir = Path(output_dir) / Path("endpoints")
    endpoint_files = generate_endpoints(api_model.tags, endpoints_dir)
    blackify_files(endpoint_files)

    models_dir = Path(output_dir) / Path("models")
    model_files = generate_models(api_model.definitions, models_dir)
    blackify_files(model_files)

    schemas_dir = Path(output_dir) / Path("schemas")
    generate_schemas(swagger, schemas_dir)


def blackify_files(path_list: List[Path]):
    for path in path_list:
        blackify_file(path)


def blackify_file(source):
    black.format_file_in_place(source, fast=True, mode=black.FileMode(), write_back=black.WriteBack.YES)


def generate_init(swagger, output_dir):
    parent_dir = Path(__file__).parent
    Path(output_dir).mkdir(exist_ok=True)
    swagger_version = swagger.get("openapi") or swagger.get("swagger")
    with open(Path(parent_dir, "templates/api_init.jinja")) as f:
        template = Template(f.read()).render(swagger_version=swagger_version, infos=swagger["info"])
    init_file = Path(output_dir, f"__init__.py")
    with open(init_file, "w") as f:
        f.write(template)
    print(f"Generated '{init_file}' file")
    return [init_file]


def generate_endpoints(tags, output_dir):
    parent_dir = Path(__file__).parent
    Path(output_dir).mkdir(exist_ok=True)
    print("Generating endpoints...")
    endpoint_files = []
    for tag in tags.values():
        with open(Path(parent_dir, "templates/paths.jinja")) as f:
            template = Template(f.read()).render(
                class_name=tag.name,
                endpoints=tag.endpoints,
                description=tag.description,
            )
        endpoint_file = Path(output_dir, f"{tag.name}.py")
        with open(endpoint_file, "w") as f:
            f.write(template)
        print(f"Generated '{endpoint_file}' file")
        endpoint_files.append(endpoint_file)
    return endpoint_files


def generate_models(definitions, output_dir):
    parent_dir = Path(__file__).parent
    Path(output_dir).mkdir(exist_ok=True)
    definition: Definition
    print("Generating models...")
    model_files = []
    for definition in definitions.values():
        Path(output_dir).mkdir(exist_ok=True)
        with open(Path(parent_dir, "templates/models.jinja")) as f:
            template = Template(f.read()).render(class_name=definition.name, properties=definition.properties)
        model_file = Path(output_dir, f"{definition.name}.py")
        with open(model_file, "w") as f:
            f.write(template)
        print(f"Generated '{model_file}' file")
        model_files.append(model_file)
    return model_files


def generate_schemas(swagger, output_dir):
    Path(output_dir).mkdir(exist_ok=True)
    print("Generating schemas...")
    schema_files = []
    for schema_name, schema in swagger["definitions"].items():
        Path(output_dir).mkdir(exist_ok=True)
        schema_file = Path(output_dir, f"{schema_name}.json")
        with open(schema_file, "w") as f:
            f.write(json.dumps(schema, indent=4))
            f.write("\n")
        print(f"Generated '{schema_file}' file")
        schema_files.append(schema_file)
    return schema_files
