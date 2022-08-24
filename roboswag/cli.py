from pathlib import Path
from typing import Optional

import rich_click as click

from roboswag.auth import AUTH_BACKENDS
from roboswag.generate import generate_libraries
from roboswag.version import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class AuthBackend(click.ParamType):
    name = "authorization"

    def convert(self, value, param, ctx):
        backends = {backend.lower(): auth_class for backend, auth_class in AUTH_BACKENDS.items()}
        normalized = value.casefold()
        if normalized in backends:
            return backends[normalized]
        backend_names = "\n    ".join(backend for backend in AUTH_BACKENDS.keys())
        self.fail(
            f"Invalid authorization backend: {value}. Authorization can be only one of:\n    {backend_names}",
            param,
            ctx,
        )


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="roboswag")
def cli():
    """
    Roboswag is a tool that generates Python libraries out of your Swagger (OpenAPI specification file).
    """
    pass


@cli.command()
@click.option(
    "-s",
    "--spec",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        path_type=str,
    ),
    required=True,
    metavar="SWAGGER",
    help="OpenAPI specification file",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        writable=True,
        allow_dash=False,
        path_type=Path,
    ),
    show_default="current working directory",
    metavar="OUTPUT_DIR",
    help="Output directory path",
)
@click.option(
    "-a",
    "--authorization",
    type=AuthBackend(),
    show_default="Authorization found in the specification",
    metavar="AUTH_CLASS",
    help="Overwrite default authorization class",
)
def generate(spec: str, output_dir: Optional[Path] = None, authorization: Optional[Path] = None):
    """Generate Python libraries."""
    generate_libraries(spec, output_dir, authorization)
