from pathlib import Path
from typing import Optional

from jinja2 import Template

from openapi.generate.models.api import APIModel


def generate(source, output: Optional[Path] = None):
    api_model = APIModel.from_swagger(source)
    output_dir = api_model.name
    if output is not None:
        output_dir = output / output_dir
    Path(output_dir).mkdir(exist_ok=True)
    for tag in api_model.tags.values():
        parent_dir = Path(__file__).parent
        with open(Path(parent_dir, "template.template")) as f:
            template = Template(f.read()).render(
                class_name=tag.name, endpoints=tag.endpoints, description=tag.description
            )
        with open(Path(output_dir, f"{tag.name}.py"), "w") as f:
            f.write(template)
        print(f"Generated {output_dir}/{tag.name} file")
