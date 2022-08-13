import rich_click as click

from roboswag.generate import generate_libraries
from roboswag.version import __version__

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


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
def generate(spec: str):
    """Generate Python libraries."""
    generate_libraries(spec)
