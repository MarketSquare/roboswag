import argparse
import sys
from importlib.metadata import version

from roboswag.generate.generate import generate

try:
    __version__ = version("roboswag")
except Exception:  # pragma: no cover
    pass


def generate_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spec", metavar="SWAGGER", help="OpenAPI specification file")
    parser.add_argument(
        "-v", "--version", action="version", version=__version__, help="display Roboswag version and exit"
    )
    args = parser.parse_args()
    if not args.spec:
        print("Please provide specification file with '-s' option")
        sys.exit(1)
    generate(args.spec)


def run_roboswag():
    generate_cli()
