import json
from pathlib import Path
from typing import Optional

from jinja2 import Template

from openapi.generate.models.api import APIModelCreator
from openapi.generate.models.definition import Definition


def generate(source, output: Optional[Path] = None):
    api_model, swagger = APIModelCreator.from_prance(source)
    output_dir = api_model.name
    if output is not None:
        output_dir = output / output_dir
    Path(output_dir).mkdir(exist_ok=True)

    generate_init(swagger, output_dir)

    generate_endpoints(api_model.tags, output_dir)

    models_dir = Path(output_dir) / Path("models")
    generate_models(api_model.definitions, models_dir)

    schemas_dir = Path(output_dir) / Path("schemas")
    generate_schemas(swagger, schemas_dir)


def generate_init(swagger, output_dir):
    parent_dir = Path(__file__).parent
    Path(output_dir).mkdir(exist_ok=True)
    swagger_version = swagger.get("openapi") or swagger.get("swagger")
    with open(Path(parent_dir, "templates/api_init.jinja")) as f:
        template = Template(f.read()).render(swagger_version=swagger_version, infos=swagger["info"])
    with open(Path(output_dir, f"__init__.py"), "w") as f:
        f.write(template)
    print(f"Generated '{output_dir}\\__init__.py' file")


def generate_endpoints(tags, output_dir):
    parent_dir = Path(__file__).parent
    Path(output_dir).mkdir(exist_ok=True)
    print("Generating endpoints...")
    for tag in tags.values():
        with open(Path(parent_dir, "templates/paths.jinja")) as f:
            template = Template(f.read()).render(
                class_name=tag.name,
                endpoints=tag.endpoints,
                description=tag.description,
            )
        with open(Path(output_dir, f"{tag.name}.py"), "w") as f:
            f.write(template)
        print(f"Generated '{output_dir}\\{tag.name}.py' file")


def generate_models(definitions, output_dir):
    parent_dir = Path(__file__).parent
    Path(output_dir).mkdir(exist_ok=True)
    definition: Definition
    print("Generating models...")
    for definition in definitions.values():
        Path(output_dir).mkdir(exist_ok=True)
        with open(Path(parent_dir, "templates/models.jinja")) as f:
            template = Template(f.read()).render(class_name=definition.name, properties=definition.properties)
        with open(Path(output_dir, f"{definition.name}.py"), "w") as f:
            f.write(template)
        print(f"Generated '{output_dir}\\{definition.name}.py' file")


def generate_schemas(swagger, output_dir):
    Path(output_dir).mkdir(exist_ok=True)
    print("Generating schemas...")
    for schema_name, schema in swagger["definitions"].items():
        Path(output_dir).mkdir(exist_ok=True)
        with open(Path(output_dir, f"{schema_name}.json"), "w") as f:
            f.write(json.dumps(schema))
            f.write("\n")
        print(f"Generated '{output_dir}\\{schema_name}.json' file")
