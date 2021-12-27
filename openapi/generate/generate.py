from pathlib import Path
from typing import Optional

from jinja2 import Template

from openapi.generate.models.api import APIModelCreator
from openapi.generate.models.definition import Definition


def generate(source, output: Optional[Path] = None):
    # TODO: Add API module init file with details from API info as docstring
    api_model = APIModelCreator.from_prance(source)
    output_dir = api_model.name
    if output is not None:
        output_dir = output / output_dir
    Path(output_dir).mkdir(exist_ok=True)
    for tag in api_model.tags.values():
        parent_dir = Path(__file__).parent
        with open(Path(parent_dir, "templates/template.template")) as f:
            template = Template(f.read()).render(
                class_name=tag.name, endpoints=tag.endpoints, description=tag.description
            )
        with open(Path(output_dir, f"{tag.name}.py"), "w") as f:
            f.write(template)
        print(f"Generated '{output_dir}\\{tag.name}' file")

    definition: Definition
    for definition in api_model.definitions.values():
        defs_dir = Path(output_dir) / Path("schemas")
        Path(defs_dir).mkdir(exist_ok=True)
        with open(Path(parent_dir, "templates/definitions.template")) as f:
            template = Template(f.read()).render(
                class_name=definition.name, properties=definition.properties
            )
        with open(Path(defs_dir, f"{definition.name}.py"), "w") as f:
            f.write(template)
        print(f"Generated '{defs_dir}\\{definition.name}' file")
