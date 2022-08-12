import rich_click as click

from roboswag.generate.generate import generate
from roboswag.version import __version__


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="roboswag")
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
def cli(spec: str):
    """
    Roboswag is a tool that generates Python libraries out of your Swagger (OpenAPI specification file).
    """
    generate(spec)
